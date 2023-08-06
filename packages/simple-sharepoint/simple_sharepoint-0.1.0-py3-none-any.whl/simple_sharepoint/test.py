from sharepoint import Client




if __name__ == "__main__":
    cid = "ea5065fa-b6c0-48a9-8786-3f75d5fc7fdf"
    csec = "b3besXGrBW/qi9I6Gb0FqGd2EzJcs3W/iohRV6Ns1qI="

    base_url = "https://wellbia.sharepoint.com/sites/Wellbia.comCo.Ltd/"
    default_path = "/sites/Wellbia.comCo.Ltd/Shared Documents"
    c = Client(cid, csec, base_url)

    # c.upload_file("C:\\Users\\sprumin\\Desktop\\FlyVPN.lnk", f"{default_path}/테스트/A/B/C")
    # c.upload_dir("D:\\files\\test", f"{default_path}/테스트")
    # c.download_file(f"{default_path}/테스트/A/a/b.txt", "D:\\files\\test\\b.txt")
    c.download_dir(f"{default_path}/테스트", "D:\\files\\test")

    