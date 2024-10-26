# VaultEnv

A simple script to pull env vars from hashicorp vault for developers

## Set up the Vault CLI
On ubuntu run the following, otherwise refer to [install vault](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-install)

```bash
sudo apt update
sudo apt install gpg wget
sudo apt install jq
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault
```

Export the vault address and disable TLS cert check

```bash
export VAULT_ADDR=https://vault.tail9ec9c.ts.net:8200
export VAULT_SKIP_VERIFY=true
```

You can now log in and use the vault CLI from your local machine

```bash
vault login -method=github token=xXxXxXxXxX
```

## Install and use VaultEnv

Install the app using:
```bash
pip install pyvaultenv
```

## Usage

Run `vaultenv -h` to see the help menu

### Basic usage

Run the `vaultenv` command followed by as many paths as you want to parse the env files.

Paths you provide should either be a path to a folder containing a `.env.template` file or a path to an env template file.

e.g. 
```bash
vaultenv ./folder_containing_.env_file/ ./.custom_env_file
```

### Creating env files template

In your .env file template, you can specify either:
- A static env var, the key should be uppercase. `<ENV_VAR_NAME>=<ENV_VAR_VALUE>`
- A vault secret path, the key should be lowercase. `<vault_secret_path>.<vault_secret_key_or_wildcard>`

e.g.
```env
MY_STATIC_VAR=static_value
developer/my_secret.secret_key
developer/my_other_secret.*
```

### Custom token & url

The default URL for the vault server is set on the tailscaile IP.
The default vault token dir is set to `~/.vault-token`, this is the default location used by the vault cli.

If you really need to change these values, use the `--vault-url` and `--token-path` flags.
For example:
```bash
vaultenv --vault-url http://my_vault:8200 --token-path ~/.my_vault_token
```

If you want you can directly specify the token in the command line using the `--token` flag.
