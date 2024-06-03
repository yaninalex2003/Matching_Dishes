const fs = require("fs");
const crypto = require("crypto");
const yaml = require("js-yaml");

const readline = require("readline").createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: true,
});

async function startWaiting(id, config_secrets, config_gpt, dish) {
  setTimeout(async () => {
    const res = await fetch(`https://operation.api.cloud.yandex.net/operations/${id}`, {
      headers: {
        'Authorization': `Bearer ${config_secrets.iam_token}`
      }
    });
    const content = await res.text();
    if (JSON.parse(content).done === true) {
      const name = `text${crypto.randomBytes(10).toString('hex')}.txt`;
      var fd = fs.openSync(`${config_gpt.generated_data_path}/${name}`, "w");
      fs.writeFileSync(fd, dish);
      fs.writeFileSync(fd, '\n-------------------\n');
      fs.writeFileSync(fd, JSON.parse(content).response.alternatives[0].message.text);
      fs.closeSync(fd);
      console.log(`Created ${config_gpt.generated_data_path}/${name}`);

    } else {
      console.log(`Waiting ${id} ...`);
      startWaiting(id, config_secrets, config_gpt, dish);
    }
  }, 5000);
}

async function genAnalogues(name) {
  const config_secrets = yaml.load(fs.readFileSync("../ya_gpt_secrets.yaml", 'utf8'));
  const config_gpt = yaml.load(fs.readFileSync("../gen_settings.yaml", 'utf8'));

  const pfd = fs.openSync(`${config_gpt.generated_data_path}/prompt/${name}`, "r");
  try {
    const textdata = fs.readFileSync(pfd).toString();
    const l = textdata.indexOf('[');
    const r = textdata.lastIndexOf(']');
    const data = `{ "data": ${textdata.substring(l, r + 1)} }`;
    const prompts = JSON.parse(data);
    fs.closeSync(pfd);

    for (var i = 0; i < prompts.data.length; i++) {
      const entry = prompts.data[i];
      var prompt = {
        "modelUri": `gpt://${config_secrets.folder_id}/yandexgpt`,
        "completionOptions": {
          "stream": false,
          "temperature": config_gpt.prompts.generate_analogues.temperature,
          "maxTokens": "4000"
        },
        "messages": [
          {
            "role": "system",
            "text": config_gpt.prompts.generate_analogues.system
          },
          {
            "role": "user",
            "text": `Переформулируй название ресторанного блюда.: ${entry.dish} и напиши сколько в нем калорий, белков, жиров и углеводов в граммах на 100 грамм продукта. Ответ должен содеражать 5 альтернативных названий блюда`
          }
        ]
      };

      const res = await fetch("https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${config_secrets.iam_token}`,
          'x-folder-id': config_secrets.folder_id
        },
        body: JSON.stringify(prompt)
      });

      const content = await res.text();
      const id = JSON.parse(content).id;

      startWaiting(id, config_secrets, config_gpt, entry.dish);
    }
  } catch {
    console.log("failure");
  }
}

async function genDishes() {
  const config_secrets = yaml.load(fs.readFileSync("../ya_gpt_secrets.yaml", 'utf8'));
  const config_gpt = yaml.load(fs.readFileSync("../gen_settings.yaml", 'utf8'));

  var prompt = {
    "modelUri": `gpt://${config_secrets.folder_id}/yandexgpt`,
    "completionOptions": {
      "stream": false,
      "temperature": config_gpt.prompts.generate_dishes.temperature,
      "maxTokens": "4000"
    },
    "messages": [
      {
        "role": "system",
        "text": config_gpt.prompts.generate_dishes.system
      },
      {
        "role": "user",
        "text": config_gpt.prompts.generate_dishes.user
      }
    ]
  };

  const res = await fetch("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${config_secrets.iam_token}`,
      'x-folder-id': config_secrets.folder_id
    },
    body: JSON.stringify(prompt)
  });

  const content = await res.text();
  const text = JSON.parse(content).result.alternatives[0].message.text;

  if (!fs.existsSync(`${config_gpt.generated_data_path}`)) {
    fs.mkdirSync(`${config_gpt.generated_data_path}`);
  }
  if (!fs.existsSync(`${config_gpt.generated_data_path}/prompt`)) {
    fs.mkdirSync(`${config_gpt.generated_data_path}/prompt`);
  }
  const name = crypto.randomBytes(10).toString('hex');
  const fd = fs.openSync(`${config_gpt.generated_data_path}/prompt/${name}`, 'w');
  fs.writeFileSync(fd, text);
  fs.closeSync(fd);
  console.log(`Created ${config_gpt.generated_data_path}/prompt/${name}`);
  return name;
}

async function main() {
  const name = await genDishes();
  genAnalogues(name);
}

main();
