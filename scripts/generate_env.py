def prompt_env_var(var_name, default=None, secret=False):
    prompt_text = f"{var_name}"
    if default:
        prompt_text += f" [{default}]"
    prompt_text += ": "

    if secret:
        import getpass

        value = getpass.getpass(prompt_text)
    else:
        value = input(prompt_text)

    if not value and default is not None:
        value = default
    return value


def main():
    print("This script will help generate a .env file for the project.")
    env_vars = {}

    env_vars["SECRET_KEY"] = prompt_env_var("SECRET_KEY", default="secret", secret=True)
    env_vars["DEBUG"] = prompt_env_var("DEBUG", default=True)
    env_vars["MYSQL_ROOT_PASSWORD"] = prompt_env_var("MYSQL_ROOT_PASSWORD", default="docker", secret=True)
    env_vars["MYSQL_DATABASE"] = prompt_env_var("MYSQL_DATABASE", default="ecommerce_db")
    env_vars["MYSQL_USER"] = prompt_env_var("MYSQL_USER", default="test_mart")
    env_vars["MYSQL_PASSWORD"] = prompt_env_var("MYSQL_PASSWORD", secret=True)
    env_vars["DB_HOST"] = prompt_env_var("DB_HOST", default="db")
    env_vars["DB_PORT"] = prompt_env_var("DB_PORT", default="3306")

    env_vars["DATABASE_URL"] = (
        f"mysql+pymysql://{env_vars['MYSQL_USER']}:"
        f"{env_vars['MYSQL_PASSWORD']}@{env_vars['DB_HOST']}:{env_vars['DB_PORT']}/{env_vars['MYSQL_DATABASE']}"
    )

    with open(".env", "w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")

    print("\n.env file created successfully!")


if __name__ == "__main__":
    main()
