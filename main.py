import os
import struct

def read_boot_sector(drive):
    with open(f"\\\\.\\{drive}", "rb") as f:
        boot_sector = f.read(512)
    return boot_sector

def parse_boot_sector(boot_sector):
    oem_id = boot_sector[3:11].decode('utf-8')
    if "NTFS" in oem_id:
            id = oem_id
    elif "MSDOS" in oem_id or "FAT" in oem_id:
            id = boot_sector[82:87].decode('utf-8')

    if "FAT" in id:
         bytes_per_sector = struct.unpack_from("<h", boot_sector, 11)[0]
         sectors_per_cluster = boot_sector[13]
         number_of_reserved_sectors = struct.unpack_from("<h", boot_sector, 14)[0]
         number_of_heads = struct.unpack_from("<h", boot_sector, 16)[0]
         number_of_entry = struct.unpack_from("<h", boot_sector, 17)[0] 
         number_of_sector = struct.unpack_from("<h", boot_sector, 22)[0]
         sizebyte = boot_sector[32:36]
         size_vol = int.from_bytes(sizebyte, byteorder='little')
         name_vol = boot_sector[71:81].decode('utf-8')
         
    else:
         bytes_per_sector = struct.unpack_from("<h", boot_sector, 11)[0]
         sectors_per_cluster = boot_sector[13]
         number_of_reserved_sectors = struct.unpack_from("<h", boot_sector, 14)[0]
         number_of_heads = ""
         number_of_entry = ""
         size_vol = ""
         name_vol = ""
    
    return {
        "   id_filesystem": id,
        "   bytes_per_sector": bytes_per_sector,
        "   sectors_per_cluster": sectors_per_cluster,
        "   number_of_reserved_sectors": number_of_reserved_sectors,
        "   number_of_heads": number_of_heads,
        "   number_of_entry": number_of_entry,
        "   size(MB)": size_vol,
        "   name": name_vol
    }

def read_sector(drive, sector):
    with open(f"\\\\.\\{drive}", "rb") as f:
        f.seek(sector * 512)
        return f.read(512)
def create_image_file(drive, output_file):
    with open(output_file, "wb") as f:
        print("Vui lòng chờ....")
        for sector in range(1, 1024):
            data = read_sector(drive, sector)
            f.write(data)

if __name__ == "__main__":
    print("")
    volview = input("Nhập tên volume cần xem thông tin (C/D/E/F/G...): ") 
    drive = volview + ":"
    boot_sector = read_boot_sector(drive)
    info = parse_boot_sector(boot_sector)
    print("Thông tin từ BootSector:")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("")
    volIMG = input("Nhập tên volume cần tạo IMAGE (C/D/E/F/G...): ") 
    drive = volIMG + ":"
    output_file = "image"+ volIMG + ".bin"
    create_image_file(drive, output_file)
    print("Thành công!")
