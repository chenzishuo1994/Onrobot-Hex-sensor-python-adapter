import socket
import time
import threading
import codecs
import binascii


def signed_bin2dec(bin_str: str) -> int:
    bin_str = bin_str.strip()
    if (bin_str[:2] == '0b'):
        if (bin_str[2] == '_'):
            bin_str = bin_str[3:]
        else:
            bin_str = bin_str[2:]
    if (bin_str[0] == '_'):
        int('输入 ' + bin_str + ' 不合法，首字符不能是下划线 且 不允许出现连续两个下划线')
    elif (bin_str[0] == '0'):
        return int(bin_str, base=2)
    elif (bin_str[0] == '1'):
        a = int(bin_str, base=2)  # 此语句可检查输入是否合法
        bin_str = bin_str.replace('_', '')
        return a - 2 ** len(bin_str)
    else:
        int('输入 ' + bin_str + ' 不合法，必须为2进制补码，不允许带正负号')


def oneHex2fourBin(one_hex: str) -> str:
    if (one_hex == '0'):
        return '0000'
    elif (one_hex == '1'):
        return '0001'
    elif (one_hex == '2'):
        return '0010'
    elif (one_hex == '3'):
        return '0011'
    elif (one_hex == '4'):
        return '0100'
    elif (one_hex == '5'):
        return '0101'
    elif (one_hex == '6'):
        return '0110'
    elif (one_hex == '7'):
        return '0111'
    elif (one_hex == '8'):
        return '1000'
    elif (one_hex == '9'):
        return '1001'
    elif (one_hex == 'a' or one_hex == 'A'):
        return '1010'
    elif (one_hex == 'b' or one_hex == 'B'):
        return '1011'
    elif (one_hex == 'c' or one_hex == 'C'):
        return '1100'
    elif (one_hex == 'd' or one_hex == 'D'):
        return '1101'
    elif (one_hex == 'e' or one_hex == 'E'):
        return '1110'
    elif (one_hex == 'f' or one_hex == 'F'):
        return '1111'
    else:
        int('输入16进制字符' + one_hex + '错误，16进制只能包含0~9, a~f或A~F')


def signed_hex2bin(hex_str: str, bin_width: int = -1) -> str:
    input_hex_str = hex_str
    hex_str = hex_str.strip()
    # 检查输入是否合法，不允许带正负号，首尾不能是下划线，不能出现连续两个下划线
    if (hex_str[0] in ['+', '-', '_'] or hex_str[-1] == '_' or '__' in hex_str):
        int('输入' + input_hex_str + '不合法，必须为16进制补码，不允许带正负号, '
            + '首尾不能是下划线，不能出现连续两个下划线')
    elif (hex_str[:2] == '0x'):
        hex_str = hex_str[2:]
    hex_str = hex_str.replace('_', '')  # 输入合法则去除下划线
    bin_str = ''
    for i in hex_str:
        bin_str += oneHex2fourBin(i)
    # 去掉2进制补码字符串前面多余的符号位，保留两位
    for i in range(len(bin_str) - 1):
        if (bin_str[i + 1] == bin_str[0]):
            if (i + 1 == len(bin_str) - 1):
                bin_str = bin_str[i:]
            else:
                continue
        else:
            bin_str = bin_str[i:]
            break
    if (bin_str == '00'):
        bin_str = '0'
    if (bin_width == -1):
        pass
    elif (bin_width < len(bin_str)):
        # 实际位宽大于设定位宽则报警告，然后按实际位宽输出
        print('位宽参数' + str(bin_width) + ' < 16进制补码' + input_hex_str + '输出2进制补码'
              + '0b' + bin_str + '实际位宽' + str(len(bin_str)) + '，请修正位宽参数')
    else:
        bin_str = bin_str[0] * (bin_width - len(bin_str)) + bin_str  # 实际位宽小于设定位宽则补符号位
    return '0b' + bin_str


def signed_hex2dec(hex_str: str) -> int:
    return signed_bin2dec(signed_hex2bin(hex_str))

def udp_get():
    ip = '192.168.1.1'
    port = 49152
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    udp_socket.connect((ip,int(port)))
    inp='1234' \
        '0002' \
        '0000' \
        '0001'
    udp_socket.send(codecs.decode(inp,'hex'))
    data= udp_socket.recv(1024)
    if data:
        #print(data)
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))
        #print('来自传感器发送的数据：{}'.format( data.decode('gbk')))
        str_data = binascii.b2a_hex(data)
        new_data = str(str_data,encoding='utf-8')
        dd=new_data[24:]
        fx=signed_hex2dec(dd[0:8])/10000
        fy=signed_hex2dec(dd[8:16])/10000
        fz=signed_hex2dec(dd[16:24])/10000
        tx=signed_hex2dec(dd[24:32])/10000
        ty=signed_hex2dec(dd[32:40])/10000
        tz=signed_hex2dec(dd[40:48])/10000
    udp_socket.close()
    return fx,fy,fz,tx,ty,tz


if __name__ == '__main__':
    fx, fy, fz, tx, ty, tz = udp_get()
    print()

