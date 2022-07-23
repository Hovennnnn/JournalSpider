from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os

def check_driver_new_version(where="main"):
    # os.environ['WDM_LOCAL'] = '1'
    # os.environ['WDM_SSL_VERIFY'] = '0'
    if where == "main":
        driver_path = EdgeChromiumDriverManager(path = os.path.dirname(__file__), cache_valid_range=30).install()
        with open(os.path.join(os.path.dirname(__file__), "driver_path"), "w") as f:
            f.write(driver_path)
        return driver_path
    elif where == "import":
        with open(os.path.join(os.path.dirname(__file__), "driver_path"), "r") as f:
            driver_path = f.read()
        return driver_path
    else:
        raise RuntimeError("where参数错误！")

if __name__ == "__main__":
    print(check_driver_new_version(where="main"))
    print(check_driver_new_version(where="import"))