# Setting Up OpenCode

OpenCode is an open-source AI coding agent that works with any OpenAI-compatible API — you bring your own key and endpoint. This guide uses **GWDG Chat AI** as the provider (free for German academic institutions, GDPR-compliant, all inference in Göttingen), but the same steps apply to any other provider: just swap the `baseURL` and API key in the configuration step.

**Prerequisites for GWDG:** You have an institutional account (university or research institute) that gives you access to Chat AI via the Academic Cloud.

**Jump to your platform:** [macOS](#macos) · [Windows](#windows)

---

## macOS

> **Using a different API provider?** Skip Steps 1–4 and jump to Step 5.

### Step 1: Activate your Academic Cloud Account

1. Go to **https://academiccloud.de**
2. Click **Föderierte Anmeldung** (Federated Login) and select your institution
3. You will be redirected to your institution's login page — sign in with your usual credentials
4. On first login, accept the terms of use. Account creation takes up to 1 minute.

> You can now access Chat AI directly at **https://chat-ai.academiccloud.de** — log in with the same federated login.

---

### Step 2: Request an API Key

You need an API key to use the models programmatically (e.g. in OpenCode).

1. Go to **https://kisski.gwdg.de/leistungen/2-02-llm-service/**
2. Click **Book**
3. Log in with your Academic Cloud account
4. Fill out the form:
   - **Service type:** API access to our chat service
   - **Requirements:** Briefly describe your intended use (e.g. testing agentic coding workflows and AI-assisted research tools). Keep it short and honest.
   - **Critical data in regards to GDPR:** Answer honestly — if you plan to work with personal research data at any point, select Yes.
5. Submit the form

You will receive your API key by email, usually within one business day. The key is a 33-character hex string.

> **Important:** Never share your API key with other users. Each person should request their own.

---

### Step 3: Store your API Key

Open your terminal and run:

```bash
echo 'export GWDG_API_KEY="your-key-here"' >> ~/.zshenv
chmod 600 ~/.zshenv
source ~/.zshenv
```

Replace `your-key-here` with your actual key.

> **Why `~/.zshenv` and not `~/.zshrc`?** `~/.zshrc` is only sourced by *interactive* zsh sessions. Tools like OpenCode, VS Code's integrated terminal, or any script started from a non-interactive shell would not see your key and silently fall back to errors. `~/.zshenv` is sourced by *every* zsh invocation. The `chmod 600` restricts the file to your own user — the key sits on disk in plaintext, so this is good practice.

To verify it worked, open a fresh terminal and run:

```bash
echo $GWDG_API_KEY
```

This should print your key, not the placeholder text.

---

### Step 4: Test the Connection

Run this command to confirm your key works and the models respond:

```bash
curl -s \
  -H "Authorization: Bearer $GWDG_API_KEY" \
  -H "Content-Type: application/json" \
  -X POST "https://chat-ai.academiccloud.de/v1/chat/completions" \
  -d '{"model":"glm-4.7","messages":[{"role":"user","content":"Say hello in one sentence."}]}'
```

You should get a JSON response containing the model's reply. If you see an error, double-check that the key is set correctly.

#### View your current rate limits

```bash
curl -s -I \
  -H "Authorization: Bearer $GWDG_API_KEY" \
  "https://chat-ai.academiccloud.de/v1/chat/completions" \
  | grep -i "^x-ratelimit"
```

Look for `x-ratelimit-limit-*` and `x-ratelimit-remaining-*` headers. The official documented monthly limit for a new key is **3000 requests/month** (per [the KISSKI LLM service page](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/)). The page notes this can be increased on request — if you hit the cap, mail support@gwdg.de with a brief justification.

> **Note:** Each call to this check itself consumes one request from each rate-limit bucket, since the server-side counter increments on any authenticated request to the endpoint.

#### Get the current list of available models

```bash
curl -s -X POST \
  -H "Authorization: Bearer $GWDG_API_KEY" \
  -H "Content-Type: application/json" \
  "https://chat-ai.academiccloud.de/v1/models" \
  | jq '.data[].id'
```

> If `jq` is not installed: `brew install jq`

Copy the model IDs from the output — you will need them in Step 6.

---

### Step 5: Install OpenCode Desktop

```bash
brew install --cask opencode-desktop
```

Alternatively, download directly for your platform from **https://opencode.ai/download**.

- macOS with Apple Silicon (M1/M2/M3/M4): choose **macOS (Apple Silicon)**
- macOS with Intel chip: choose **macOS (Intel)**

The source code is available at **https://github.com/opencode-ai/opencode** (MIT license).

---

### Step 6: Configure the GWDG Provider

Open OpenCode Desktop. In the provider setup screen, fill in:

- **Anbieter-ID / Provider ID:** `gwdg` (must match exactly)
- **Anzeigename / Display name:** `GWDG Chat AI`
- **Basis-URL / Base URL:** `https://chat-ai.academiccloud.de/v1`
- **API-Schlüssel / API Key:** your key

**Alternative — edit the config file directly.** This also lets you control exactly which model IDs appear:

```bash
nano ~/.config/opencode/opencode.json
```

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "gwdg": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "GWDG Chat AI",
      "options": {
        "baseURL": "https://chat-ai.academiccloud.de/v1"
      },
      "models": {
        "glm-4.7":                            { "name": "GLM-4.7" },
        "qwen3-coder-30b-a3b-instruct":       { "name": "Qwen3 Coder 30B" },
        "devstral-2-123b-instruct-2512":      { "name": "Devstral 2 123B" },
        "qwen3.5-397b-a17b":                  { "name": "Qwen 3.5 397B" },
        "mistral-large-3-675b-instruct-2512": { "name": "Mistral Large 3" }
      }
    }
  }
}
```

Save with `Ctrl+O` → Enter → `Ctrl+X`.

---

### Step 7: Verify Traffic Goes to GWDG

With OpenCode running, open a second terminal window and run:

```bash
sudo lsof -i TCP:443 | grep opencode
```

You should see a connection to `saia.academiccloud.de` — this is the GWDG backend in Göttingen. No connections to `openai.com`, `anthropic.com`, or `opencode.ai` should appear when using your GWDG models.

---

### Step 9: Recommended Models and Use Cases

| Model ID | Best for |
|---|---|
| `glm-4.7` | **Default.** Agentic coding, tool use, fast responses |
| `qwen3-coder-30b-a3b-instruct` | Coding tasks, quick turnaround |
| `devstral-2-123b-instruct-2512` | Complex multi-file software engineering |
| `qwen3.5-397b-a17b` | Analysis, writing, German-language tasks |
| `mistral-large-3-675b-instruct-2512` | Multilingual, strong in German |

Start with **GLM-4.7** as your default. Switch models manually for specific tasks.

---

### Step 10: First Test

Open a folder with some files in OpenCode. Switch to **Plan mode** first (Tab key) — this lets the agent read and suggest changes without modifying anything. Ask:

> *"What files are in this project and what do they do?"*

If the agent reads the files and gives a coherent answer, your setup is working correctly.

---

### Data Protection Notes

- All self-hosted GWDG models process data exclusively on GWDG servers in Göttingen
- No chat history is stored server-side
- OpenCode does not store your code or context data on its own servers
- If your institution uses GWDG services on behalf of an organisation, a data processing agreement (Auftragsverarbeitungsvertrag, AVV) between your institution and GWDG is advisable — contact your institution's data protection office
- Do not use the external OpenAI models available in Chat AI when working with personal or sensitive research data

---

## Windows

> **Not tested.** These steps are based on the official OpenCode documentation and general Windows conventions. If you run into issues, check the [OpenCode docs](https://opencode.ai/docs/) or open an issue on the [OpenCode GitHub](https://github.com/opencode-ai/opencode).

> **Using a different API provider?** Skip Steps 1–4 and jump to Step 5.
---

### Step 1: Activate your Academic Cloud Account

1. Go to **https://academiccloud.de**
2. Click **Föderierte Anmeldung** (Federated Login) and select your institution
3. You will be redirected to your institution's login page — sign in with your usual credentials
4. On first login, accept the terms of use. Account creation takes up to 1 minute.

> You can now access Chat AI directly at **https://chat-ai.academiccloud.de** — log in with the same federated login.

---

### Step 2: Request an API Key

You need an API key to use the models programmatically (e.g. in OpenCode).

1. Go to **https://kisski.gwdg.de/leistungen/2-02-llm-service/**
2. Click **Book**
3. Log in with your Academic Cloud account
4. Fill out the form:
   - **Service type:** API access to our chat service
   - **Requirements:** Briefly describe your intended use (e.g. testing agentic coding workflows and AI-assisted research tools). Keep it short and honest.
   - **Critical data in regards to GDPR:** Answer honestly — if you plan to work with personal research data at any point, select Yes.
5. Submit the form

You will receive your API key by email, usually within one business day. The key is a 33-character hex string.

> **Important:** Never share your API key with other users. Each person should request their own.

---

### Step 3: Store your API Key

Open **Command Prompt** (`cmd`) and run:

```cmd
setx GWDG_API_KEY "your-key-here"
```

Replace `your-key-here` with your actual key. `setx` saves the variable permanently to your user profile — no config file to edit.

**Important:** `setx` takes effect in new terminals only. Close this Command Prompt and open a fresh one, then verify:

```cmd
echo %GWDG_API_KEY%
```

This should print your key, not the placeholder text.

> **Alternative (no terminal):** Open **Start → search "environment variables" → Edit the system environment variables → Environment Variables**. Under *User variables*, click **New** and enter `GWDG_API_KEY` as the name and your key as the value.

---

### Step 4: Test the Connection

Windows 10 and 11 include `curl.exe` built in. Open a **Command Prompt** (not PowerShell — the quoting is different) and run:

```cmd
curl -s -H "Authorization: Bearer %GWDG_API_KEY%" -H "Content-Type: application/json" -X POST "https://chat-ai.academiccloud.de/v1/chat/completions" -d "{\"model\":\"glm-4.7\",\"messages\":[{\"role\":\"user\",\"content\":\"Say hello in one sentence.\"}]}"
```

You should get a JSON response containing the model's reply. If you see an error, double-check that the key is set correctly and that you opened a fresh Command Prompt after Step 3.

#### View your current rate limits

```cmd
curl -s -I -H "Authorization: Bearer %GWDG_API_KEY%" "https://chat-ai.academiccloud.de/v1/chat/completions"
```

Look for `x-ratelimit-limit-*` and `x-ratelimit-remaining-*` headers in the output. The official documented monthly limit for a new key is **3000 requests/month** (per [the KISSKI LLM service page](https://kisski.gwdg.de/en/leistungen/2-02-llm-service/)). This can be increased on request — if you hit the cap, mail support@gwdg.de with a brief justification.

> **Note:** Each call to this check itself consumes one request from each rate-limit bucket, since the server-side counter increments on any authenticated request to the endpoint.

---

### Step 5: Install OpenCode Desktop

Go to **https://opencode.ai/download** and download the **Windows (x64)** installer. Run the downloaded `.exe` file and follow the installer.

The source code is available at **https://github.com/opencode-ai/opencode** (MIT license).

---

### Step 6: Configure the GWDG Provider

Open OpenCode Desktop. In the provider setup screen, fill in:

- **Anbieter-ID / Provider ID:** `gwdg` (must match exactly)
- **Anzeigename / Display name:** `GWDG Chat AI`
- **Basis-URL / Base URL:** `https://chat-ai.academiccloud.de/v1`
- **API-Schlüssel / API Key:** your key

**Alternative — edit the config file directly.** This also lets you control exactly which model IDs appear. Open Notepad:

```cmd
notepad %APPDATA%\opencode\opencode.json
```

If the file or folder does not exist yet, create it first:

```cmd
mkdir %APPDATA%\opencode
notepad %APPDATA%\opencode\opencode.json
```

Paste the following and save:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "gwdg": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "GWDG Chat AI",
      "options": {
        "baseURL": "https://chat-ai.academiccloud.de/v1"
      },
      "models": {
        "glm-4.7":                            { "name": "GLM-4.7" },
        "qwen3-coder-30b-a3b-instruct":       { "name": "Qwen3 Coder 30B" },
        "devstral-2-123b-instruct-2512":      { "name": "Devstral 2 123B" },
        "qwen3.5-397b-a17b":                  { "name": "Qwen 3.5 397B" },
        "mistral-large-3-675b-instruct-2512": { "name": "Mistral Large 3" }
      }
    }
  }
}
```

---

### Step 7: Verify Traffic Goes to GWDG

With OpenCode running, open a **Command Prompt** and run:

```cmd
netstat -an | findstr :443
```

You should see a connection to `saia.academiccloud.de` — this is the GWDG backend in Göttingen. No connections to `openai.com`, `anthropic.com`, or `opencode.ai` should appear when using your GWDG models.

---

### Step 9: Recommended Models and Use Cases

| Model ID | Best for |
|---|---|
| `glm-4.7` | **Default.** Agentic coding, tool use, fast responses |
| `qwen3-coder-30b-a3b-instruct` | Coding tasks, quick turnaround |
| `devstral-2-123b-instruct-2512` | Complex multi-file software engineering |
| `qwen3.5-397b-a17b` | Analysis, writing, German-language tasks |
| `mistral-large-3-675b-instruct-2512` | Multilingual, strong in German |

Start with **GLM-4.7** as your default. Switch models manually for specific tasks.

---

### Step 10: First Test

Open a folder with some files in OpenCode. Switch to **Plan mode** first (Tab key) — this lets the agent read and suggest changes without modifying anything. Ask:

> *"What files are in this project and what do they do?"*

If the agent reads the files and gives a coherent answer, your setup is working correctly.

---

### Data Protection Notes

- All self-hosted GWDG models process data exclusively on GWDG servers in Göttingen
- No chat history is stored server-side
- OpenCode does not store your code or context data on its own servers
- If your institution uses GWDG services on behalf of an organisation, a data processing agreement (Auftragsverarbeitungsvertrag, AVV) between your institution and GWDG is advisable — contact your institution's data protection office
- Do not use the external OpenAI models available in Chat AI when working with personal or sensitive research data
