# from TISControlProtocol.BytesHelper import build_packet
# import socket
# import binascii

# # build feedback packet
# packet = build_packet(
#     device_id=[1, 2],
#     operation_code=[0x20, 0x21],
#     ip_address="192.168.1.4",
#     additional_packets=[
#         0,
#         0,
#         0,  # Placeholder bytes
#         2,  # Wind Direction (index in wind_direction_dict)
#         0x41,
#         0xA0,
#         0x00,
#         0x00,  # Temperature (big-endian float, e.g., 20.0°C)
#         50,  # Humidity (50%)
#         0x41,
#         0x20,
#         0x00,
#         0x00,  # Wind Speed (big-endian float, e.g., 10.0 m/s)
#         0x41,
#         0x40,
#         0x00,
#         0x00,  # Gust Speed (big-endian float, e.g., 12.0 m/s)
#         0x00,
#         0x64,  # Rainfall (100 mm)
#         0x41,
#         0x80,
#         0x00,
#         0x00,  # Lighting (big-endian float, e.g., 16.0)
#         5,  # UV Index
#     ],
# )


# def format_hex_data(data):
#     # Convert data to hexadecimal
#     hex_data = binascii.hexlify(data).decode("utf-8")

#     # Split the hexadecimal string into pairs of characters
#     hex_pairs = [hex_data[i : i + 2] for i in range(0, len(hex_data), 2)]

#     # Join the pairs with commas
#     formatted_hex = ",".join(hex_pairs)

#     return formatted_hex


# def main():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server_address = ("0.0.0.0", 6000)
#     sock.bind(server_address)

#     print({"started server": server_address})
#     while True:
#         data, address = sock.recvfrom(4096)
#         print(f"received {len(data)} bytes from {address}")
#         print(f"Data (hex): {format_hex_data(data)}")
#         # send feedback packet
#         sock.sendto(bytes(packet), ("192.168.1.187", 6000))
#         # print the packet to be sent formatted as hex
#         print(f"Packet (hex): {format_hex_data(bytes(packet))}")


# if __name__ == "__main__":
#     main()


# # c0 a8 01 04 53 4d 41 52 54 43 4c 4f 55 44 aa aa 23 01 fe ff fe 20 21 01 02 00 00 00 02 41 a0 00 00 32 41 20 00 00 41 40 00 00 00 64 41 80 00 00 05 9f 7c

import logging
import struct

wind_direction_dict = {
    0x01: "north",
    0x02: "north east",
    0x04: "east",
    0x08: "south east",
    0x10: "south",
    0x20: "south west",
    0x40: "west",
    0x80: "north west",
}


def big_endian_to_float(value):
    binary = value.to_bytes(4, "big")
    float_value = struct.unpack(">f", binary)
    return float_value


def handle_weather_feedback(info: dict):
    """
    Handle the feedback from a health sensor.
    """
    device_id = info["device_id"]
    wind_direction = wind_direction_dict[int(info["additional_bytes"][3])]
    temperature = big_endian_to_float(
        int(
            (info["additional_bytes"][4] << 24)
            | (info["additional_bytes"][5] << 16)
            | (info["additional_bytes"][6] << 8)
            | info["additional_bytes"][7]
        )
    )
    humidity = int(info["additional_bytes"][8])
    wind_speed = big_endian_to_float(
        int(
            (info["additional_bytes"][9] << 24)
            | (info["additional_bytes"][10] << 16)
            | (info["additional_bytes"][11] << 8)
            | info["additional_bytes"][12]
        )
    )
    gust_speed = big_endian_to_float(
        int(
            (info["additional_bytes"][13] << 24)
            | (info["additional_bytes"][14] << 16)
            | (info["additional_bytes"][15] << 8)
            | info["additional_bytes"][16]
        )
    )
    rainfall = int((info["additional_bytes"][17] << 8) | (info["additional_bytes"][18]))
    lighting = big_endian_to_float(
        int(
            (info["additional_bytes"][19] << 24)
            | (info["additional_bytes"][20] << 16)
            | (info["additional_bytes"][21] << 8)
            | info["additional_bytes"][22]
        )
    )
    uv = int(info["additional_bytes"][23])

    event_data = {
        "device_id": device_id,
        "feedback_type": "health_feedback",
        "wind": wind_direction,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "gust_speed": gust_speed,
        "rainfall": rainfall,
        "lighting": lighting,
        "uv": uv,
        "additional_bytes": info["additional_bytes"],
    }
    print(event_data)


info = {
    "source_ip": [192, 168, 1, 4],
    "device_id": [1, 254],
    "device_type": [255, 254],
    "operation_code": [32, 33],
    "source_device_id": [1, 2],
    "additional_bytes": [
        0,
        0,
        0,
        2,
        65,
        160,
        0,
        0,
        50,
        65,
        32,
        0,
        0,
        65,
        64,
        0,
        0,
        0,
        100,
        65,
        128,
        0,
        0,
        5,
    ],
}

handle_weather_feedback(info=info)
