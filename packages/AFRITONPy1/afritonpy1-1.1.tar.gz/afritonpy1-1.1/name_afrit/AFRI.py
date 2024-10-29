



from hashlib import md5
import json
import random
import time
from binascii        import hexlify
from uuid            import uuid4
from requests        import request



import hashlib


class Signer:
    shift_array = "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe"
    magic = 536919696

    def md5_2x(string):
        return md5(md5(string.encode()).digest()).hexdigest()

    def rc4_encrypt(plaintext: str, key: list[int]) -> str:
        s_box = [_ for _ in range(256)]
        index = 0

        for _ in range(256):
            index = (index + s_box[_] + key[_ % len(key)]) % 256
            s_box[_], s_box[index] = s_box[index], s_box[_]

        _ = 0
        index = 0
        ciphertext = ""

        for char in plaintext:
            _ = (_ + 1) % 256
            index = (index + s_box[_]) % 256

            s_box[_], s_box[index] = s_box[index], s_box[_]
            keystream = s_box[(s_box[_] + s_box[index]) % 256]
            ciphertext += chr(ord(char) ^ keystream)

        return ciphertext

    def b64_encode(
        string,
        key_table="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    ):
        last_list = list()
        for i in range(0, len(string), 3):
            try:
                num_1 = ord(string[i])
                num_2 = ord(string[i + 1])
                num_3 = ord(string[i + 2])
                arr_1 = num_1 >> 2
                arr_2 = (3 & num_1) << 4 | (num_2 >> 4)
                arr_3 = ((15 & num_2) << 2) | (num_3 >> 6)
                arr_4 = 63 & num_3

            except IndexError:
                arr_1 = num_1 >> 2
                arr_2 = ((3 & num_1) << 4) | 0
                arr_3 = 64
                arr_4 = 64

            last_list.append(arr_1)
            last_list.append(arr_2)
            last_list.append(arr_3)
            last_list.append(arr_4)

        return "".join([key_table[value] for value in last_list])

    def filter(num_list: list):
        return [
            num_list[x - 1]
            for x in [3,5,7,9,11,13,15,17,19,21,4,6,8,10,12,14,16,18,20,
            ]
        ]

    def scramble(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s) -> str:
        return "".join(
            [
                chr(_)
                for _ in [a,k,b,l,c,m,d,n,e,o,f,p,g,q,h,r,i,s,j,
                ]
            ]
        )

    def checksum(salt_list: str) -> int:
        checksum = 64
        _ = [checksum := checksum ^ x for x in salt_list[3:]]

        return checksum

    def _x_bogus(params, user_agent, timestamp, data) -> str:

        md5_data = Signer.md5_2x(data)
        md5_params = Signer.md5_2x(params)
        md5_ua = md5(
            Signer.b64_encode(Signer.rc4_encrypt(user_agent, [0, 1, 14])).encode()
        ).hexdigest()

        salt_list = [
            timestamp,
            Signer.magic,
            64,
            0,
            1,
            14,
            bytes.fromhex(md5_params)[-2],
            bytes.fromhex(md5_params)[-1],
            bytes.fromhex(md5_data)[-2],
            bytes.fromhex(md5_data)[-1],
            bytes.fromhex(md5_ua)[-2],
            bytes.fromhex(md5_ua)[-1],
        ]

        salt_list.extend([(timestamp >> i) & 0xFF for i in range(24, -1, -8)])
        salt_list.extend([(salt_list[1] >> i) & 0xFF for i in range(24, -1, -8)])
        salt_list.extend([Signer.checksum(salt_list), 255])

        num_list = Signer.filter(salt_list)
        rc4_num_list = Signer.rc4_encrypt(Signer.scramble(*num_list), [255])

        return Signer.b64_encode(f"\x02ÿ{rc4_num_list}", Signer.shift_array)
    
def tim():
    _rticket = int(time.time() * 1000)
    ts=str(int(time.time() * 1000))[:10]
    ts1=str(int(time.time() * 1000))[:10]
    icket = int(time.time() * 1000)
    return _rticket,ts,ts1,icket

import gzip
import binascii
import random


http=["7421185094760040198:7421184511113283078:c3df63f5fd02a9ac:786100e9-614d-49ec-a222-f3b8a172f7d0:1727879356",
"7421297855677810438:7421297156823107078:f557db0b78abe266:fafddecb-58e1-41a0-909e-867694a2196e:1727905629",
"7421297862968329990:7421297110425716230:99ded624021a3c7c:29923299-19ed-4ec7-bc72-8bce97f0be6b:1727905633",
"7421297893757929221:7421297177085838854:2613a09f43042cbf:5d7377a8-84f8-4708-bc41-919d3119af4a:1727905636",
"7421297911583934213:7421297234983699974:70f936b85a1d2c94:077a01c2-c5ba-448c-9a41-2a9b362916a3:1727905641",
"7421297971087918853:7421297251223766534:137f4a7d9ec5387b:443811ed-e5d3-4044-b25d-2aec8723581e:1727905646",
"7421297968517416710:7421297365941847558:07972aa771f8404b:33267031-fe6f-46fd-9ae3-838291c0c6ef:1727905649",
"7421297962197223174:7421297278424204806:dabbabe3e6d70b8c:943ab64b-80fe-43b4-a5e0-3e6658e1138b:1727905653",
"7421298015624267525:7421297447529645573:0c9b9a89413c493b:4ce59918-c12d-4c1a-8e10-618926338241:1727905673",
"7421298101249656582:7421297307545355781:9c081521fc9400c3:71108884-adb8-47ee-adc5-faee2fd3f2f8:1727905677",
"7421298080861898501:7421297315422504454:14e3daa0f4c371c7:d6deac33-8357-4d2b-bee4-29f4a3dafd70:1727905682",
"7421298126256080645:7421297320648558085:f00a06df7c460f99:30fc5c1a-010d-4102-afc3-5197c4197878:1727905690",
"7421298112260704006:7421297496779097605:6922eba12e7a8ed6:6cfb53b2-8363-497c-995e-965cff9fed48:1727905694",
"7421298158071170822:7421297407432869381:4aee6d9f5dc2699e:23cd7d80-13e9-4015-a693-390b1f6583d9:1727905698",
"7421298165326939910:7421297357432440325:f4c63abae2d1e5ad:ac78ff44-b8a3-4181-b062-b11d032bd748:1727905703",
"7421298219100964614:7421297561207965189:dcec126be6b29a7f:48e3bb3e-b726-4792-bb13-d77427f6d94a:1727905707",
"7421298189524027141:7421297503301535238:65c93b47d8e0d6be:25e063a9-4739-43b9-a24f-ddbd78248b58:1727905710",
"7421298268988491525:7421297549028099590:20c6dc20144b39c3:1105c5e0-2b5a-45dc-81e7-161e1ae0c0de:1727905715",
"7421298220633294598:7421297637778982406:d4ade5c87b448066:0b08f964-ffb4-4b6d-bcc6-3e63b0d926e0:1727905719",
"7421298280157644550:7421297588156679685:bde73674820e3548:016c9369-dedd-4924-886e-fc599c5e1e3e:1727905723",
"7421298320419047174:7421297441117324806:31555ff6c61eea69:656e854d-1b06-498c-ba7e-8522ecc39edd:1727905730",
"7421298353935566598:7421297503302059526:b602a7b1681da3c4:638e129e-2081-4385-b21c-fe2ac1b892ef:1727905736",
"7421298376093927174:7421297532755002885:26b08079cd3db3f5:dabcf4be-55c1-4f8d-b419-fa40f56cb248:1727905739",
"7421298348815353605:7421297712244819462:c95b0e4b6c74bee8:6bfdbc83-d22b-49cf-a175-d4c245ed1eae:1727905742",
"7421298378245801734:7421297692225603077:1d8e50d5d2327521:9453bcad-a226-4d2b-b7ac-22997c934a9c:1727905746",
"7421298403495298821:7421297712244983302:5dc0db03a318cba8:00ca5cfd-795a-480f-8118-c0da7c70e169:1727905749",
"7421298362656769798:7421297704984512005:be46a81b5b41735b:45a26326-3fb5-4741-b519-50ad43ea3712:1727905753",
"7421298434055636742:7421297646251378182:85c643b37f76cfef:3452859c-bdd1-49b0-b236-6ca238d9fbda:1727905758",
"7421298434362263301:7421297733589550598:806294c12c981a52:19bc8f73-c153-4f45-b187-a486b8319c48:1727905762",
"7421298458197509893:7421297616594519557:ffbfdb7af7eb496e:921a4a5b-9ee4-45d6-84b9-f2e7ad3ac30f:1727905765",
"7421298448748906246:7421297721837258246:3425fe8feded0c81:ff50bbd5-8a85-488a-97df-8b581be1c614:1727905769",
"7421298530335328005:7421297873423386117:b686d65dffb75d40:b635f898-ca11-422e-8ea0-bcadc5a85a98:1727905775",
"7421298547665995526:7421297575893321222:84593af3fa7636f9:65b55f15-42f2-4f3b-9af9-cf74335df3e8:1727905780",
"7421298523273348870:7421297710161511941:5f8132606f5d2346:bf4460b2-2a72-4615-839d-72a0eb7dd41c:1727905783",
"7421298569246246662:7421297575893452294:68ba63859a42d879:4539108b-6147-4749-b062-16bcea71068c:1727905787",
"7421298552763320069:7421297893566318086:cbe4464442323b76:0e9ece96-7a6b-4c96-9db8-231830e1026e:1727905791",
"7421298591304599302:7421297821745808902:bc421655347a7ef4:ec59c865-cf56-4b7d-a6a2-e13f94ad4a3c:1727905796",
"7421298593925351174:7421297809108354565:94f057ab5b20048f:bc7d2014-9652-4a4f-b9eb-dc3ecc9a6e77:1727905799",
"7421298577568466694:7421297767811565061:8e0e8fcb498df580:3aad5f12-6181-474b-9df9-d83abcd23447:1727905803",
"7421298666125707014:7421297877588444678:1b045f66261b97fd:200e0a75-38ae-4e45-bafc-7cd9bdac637c:1727905807",
"7421298661139351301:7421298040025302534:01384d3c6f31b8cf:9083ea97-ea5e-4d63-8113-20af0805ad27:1727905814",
"7421298680156833541:7421298040830739973:4f49c71380b8922e:4c7a312f-9796-4eaf-b71a-d455418b27bb:1727905818",
"7421298759428032262:7421298099764626950:b27852a934a2dbae:6d69ca9c-6b23-469a-acfd-a952aa8b22c1:1727905825",
"7421298729652864774:7421297821893133830:57089b6900ec182b:ace86f76-e89c-4f01-9a67-333a3e9990fc:1727905828",
"7421298719792842501:7421297920153486853:7d21cae31d1a34aa:d047a8f5-3e25-4f99-b2ea-c3356f5c89f5:1727905832",
"7421298808413374214:7421298014432413190:7f9f56cef59547ef:5d8f6658-f105-4364-a6f3-b019a65bff52:1727905838",
"7421298784787498758:7421297924399482374:e969c38cdb7e62d4:c8e92021-3546-4104-9bc5-bd3aabea5f90:1727905841",
"7421298777334728453:7421298053657003526:5bba66aa6a547c41:a119479b-6d39-4da6-b1bf-9d334f930f8f:1727905847",
"7421298765640484614:7421298069252326918:8fe740ffadaa8edd:091eed31-d9fc-4d4b-83c8-3b0a722dbc9b:1727905849",
"7421298823610517254:7421298030186612229:5a1b49c54299e704:623247d2-b316-474b-8a42-069e30358149:1727905853",
]


def device_register() -> dict:
      _rticket,ts,ts1,icket=tim()
      openudid = hexlify(random.randbytes(8)).decode()
      cdid = str(uuid4())
      google_aid = str(uuid4())
      clientudid = str(uuid4())
      req_id = str(uuid4())
      url = f"https://log-va.tiktokv.com/service/2/device_register/?ac=wifi&channel=googleplay&aid=1233&app_name=musical_ly&version_code=170404&version_name=17.4.4&device_platform=android&ab_version=17.4.4&ssmix=a&device_type=SM-G611M&device_brand=samsung&language=en&os_api=28&os_version=9&openudid={openudid}&manifest_version_code=2021704040&resolution=720*1280&dpi=320&update_version_code=2021704040&_rticket={icket}&_rticket={_rticket}&storage_type=2&app_type=normal&sys_region=US&appTheme=light&pass-route=1&pass-region=1&timezone_name=Europe%252FBerlin&cpu_support64=false&host_abi=armeabi-v7a&app_language=en&ac2=wifi&uoo=1&op_region=US&timezone_offset=3600&build_number=17.4.4&locale=en&region=US&ts={ts}&cdid={cdid}"
      
      payload = {"magic_tag":"ss_app_log","header":{"display_name":"TikTok","update_version_code":2021704040,"manifest_version_code":2021704040,"app_version_minor":"","aid":1233,"channel":"googleplay","package":"com.zhiliaoapp.musically","app_version":"17.4.4","version_code":170404,"sdk_version":"2.12.1-rc.5","sdk_target_version":29,"git_hash":"050d489d","os":"Android","os_version":"9","os_api":28,"device_model":"SM-G611M","device_brand":"samsung","device_manufacturer":"samsung","cpu_abi":"armeabi-v7a","release_build":"e1611c6_20200824","density_dpi":320,"display_density":"xhdpi","resolution":"1280x720","language":"en","timezone":1,"access":"wifi","not_request_sender":0,"mcc_mnc":"26203","rom":"G611MUBS6CTD1","rom_version":"PPR1.180610.011","cdid":cdid,"sig_hash":"e89b158e4bcf988ebd09eb83f5378e87","gaid_limited":0,"google_aid":google_aid,"openudid":openudid,"clientudid":clientudid,"region":"US","tz_name":"Europe\\/Berlin","tz_offset":7200,"oaid_may_support":False,"req_id":req_id,"apk_first_install_time":1653436407842,"is_system_app":0,"sdk_flavor":"global"},"_gen_time":1653464286461}
      
      headers = {
        "Host": "log-va.tiktokv.com",
        "accept-encoding": "gzip",
        "sdk-version": "2",
        "passport-sdk-version": "17",
        "content-type": "application/octet-stream",
        "user-agent": "okhttp/3.10.0.1"
      }
      response = request("POST", url, headers=headers, json=payload).json()

      try:
       install_id = response["install_id_str"]
       device_id = response["device_id_str"]
       ti=response['server_time']
       return install_id,device_id,openudid,cdid,ti
      except:
        rfr=random.choice(http)
        install_id=rfr.split(':')[0]
        device_id=rfr.split(':')[1].split(':')[0]
        openudid=rfr.split(':')[2].split(':')[0]
        cdid=rfr.split(':')[3].split(':')[0]
        ti=rfr.split(':')[4]
      
        return install_id,device_id,openudid,cdid,ti


class Xgorgon:
    def __init__(self, params: str, data: str) -> None:

        self.params = params
        self.data = data
        self.cookies = None

    def hash(self, data: str) -> str:
        _hash = str(hashlib.md5(data.encode()).hexdigest())

        return _hash

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = (
            base_str + self.hash(self.data) if self.data else base_str + str("0" * 32)
        )
        base_str = (
            base_str + self.hash(self.cookies)
            if self.cookies
            else base_str + str("0" * 32)
        )

        return base_str

    def get_value(self) -> json:
        base_str = self.get_base_string()

        return self.encrypt(base_str)

    def encrypt(self, data: str) -> json:
        unix = int(time.time())
        len = 0x14
        key = [
            0xDF,
            0x77,
            0xB9,
            0x40,
            0xB9,
            0x9B,
            0x84,
            0x83,
            0xD1,
            0xB9,
            0xCB,
            0xD1,
            0xF7,
            0xC2,
            0xB9,
            0x85,
            0xC3,
            0xD0,
            0xFB,
            0xC3,
        ]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0x0, 0x6, 0xB, 0x1C])

        H = int(hex(unix), 16)

        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)

        eor_result_list = []

        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(len):

            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D

            F = self.rbit_algorithm(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H

        result = ""
        for param in eor_result_list:
            result += self.hex_string(param)

        return {"X-Gorgon": ("0404b0d30000" + result), "X-Khronos": str(unix)}
    def rbit_algorithm(self, num):
        result = ""
        tmp_string = bin(num)[2:]

        while len(tmp_string) < 8:
            tmp_string = "0" + tmp_string

        for i in range(0, 8):
            result = result + tmp_string[7 - i]

        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]

        if len(tmp_string) < 2:
            tmp_string = "0" + tmp_string

        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)

        return int(tmp_string[1:] + tmp_string[:1], 16)