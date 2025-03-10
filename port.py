#!/usr/bin/env python3


from argparse import ArgumentParser
from dataclasses import dataclass
import sys
from typing import Dict, List


@dataclass
class Section:
    start: int
    end: int

    def __contains__(self, address):
        return self.start <= address < self.end

@dataclass
class SrcBinary:
    start: Dict[str, int]
    sections: List[Section]

    def __contains__(self, address):
        return any(address in section for section in self.sections)

@dataclass
class DstBinary:
    start: int
    end: int

@dataclass
class Chunk:
    src_start: int
    src_end: int
    dst_start: int

    def __contains__(self, address):
        return self.src_start <= address < self.src_end

    def port(self, address):
        return address - self.src_start + self.dst_start


SRC_BINARIES = {
    'dol': SrcBinary(
        {
            'P': 0x80004000,
            'E': 0x80004000,
            'J': 0x80004000,
            'K': 0x80004000,
        },
        [
            Section(0x80004000, 0x80006460),
            Section(0x80006460, 0x80006a20),
            Section(0x80006a20, 0x800072c0),
            Section(0x800072c0, 0x80244de0),
            Section(0x80244de0, 0x80244e90),
            Section(0x80244ea0, 0x80244eac),
            Section(0x80244ec0, 0x80258580),
            Section(0x80258580, 0x802a4040),
            Section(0x802a4080, 0x80384c00),
            Section(0x80384c00, 0x80385fc0),
            Section(0x80385fc0, 0x80386fa0),
            Section(0x80386fa0, 0x80389140),
            Section(0x80389140, 0x8038917c),
        ],
    ),
    'rel': SrcBinary(
        {
            'P': 0x805102e0,
            'E': 0x8050bf60,
            'J': 0x8050fc60,
            'K': 0x804fe300,
        },
        [
            Section(0x805103b4, 0x8088f400),
            Section(0x8088f400, 0x8088f704),
            Section(0x8088f704, 0x8088f710),
            Section(0x8088f720, 0x808b2bd0),
            Section(0x808b2bd0, 0x808dd3d4),
            Section(0x809bd6e0, 0x809c4f90),
        ],
    ),
}

DST_BINARIES = {
    'P': {
        'dol': DstBinary(0x80004000, 0x8038917c),
        'rel': DstBinary(0x80399180, 0x8076db50),
    },
    'E': {
        'dol': DstBinary(0x80004000, 0x80384dfc),
        'rel': DstBinary(0x80394e00, 0x807693f0),
    },
    'J': {
        'dol': DstBinary(0x80004000, 0x80388afc),
        'rel': DstBinary(0x80398b00, 0x8076cc90),
    },
    'K': {
        'dol': DstBinary(0x80004000, 0x8037719c),
        'rel': DstBinary(0x803871a0, 0x8075bfd0),
    },
}

CHUNKS = {
    'E': [
        Chunk(0x80004000, 0x80008004, 0x80004000),
        Chunk(0x800080f4, 0x8000ac50, 0x800080b4),
        Chunk(0x8000af78, 0x8000b6b4, 0x8000aed8),
        Chunk(0x8000c174, 0x80021ba8, 0x8000b614),
        Chunk(0x80021bb0, 0x80225f14, 0x80021b10),
        Chunk(0x80226464, 0x802402e0, 0x802260e0),
        Chunk(0x80240e18, 0x80244dd4, 0x8023ff5c),
        Chunk(0x802a4080, 0x80384c18, 0x8029fd00),
        Chunk(0x80385fc0, 0x80386008, 0x80381c40),
        Chunk(0x80386638, 0x80386644, 0x803822b8),
        Chunk(0x80386f48, 0x80386f90, 0x80382bc0),
        Chunk(0x805103b4, 0x80510a90, 0x8050c034),
        Chunk(0x80510b84, 0x8052d298, 0x8050c710),
        Chunk(0x8052d298, 0x8052d96c, 0x8054f800),
        Chunk(0x8052d96c, 0x8053d97c, 0x80528e24),
        Chunk(0x8053d97c, 0x8053e370, 0x8054fed4),
        Chunk(0x8053e370, 0x8054fb2c, 0x80538e34),
        Chunk(0x8054fb2c, 0x80550548, 0x805508c8),
        Chunk(0x80550548, 0x805537cc, 0x8054a5f0),
        Chunk(0x80553894, 0x8055572c, 0x8054d874),
        Chunk(0x8055572c, 0x8056ab6c, 0x805513ac),
        Chunk(0x8056ab6c, 0x8056b63c, 0x805ae0e8),
        Chunk(0x8056b63c, 0x80574030, 0x805667ec),
        Chunk(0x80574030, 0x805758ac, 0x805aebb8),
        Chunk(0x80575a44, 0x80583f2c, 0x8056f1e0),
        Chunk(0x80583f2c, 0x8059b5a4, 0x8057d708),
        Chunk(0x8059b5a4, 0x8059eaa4, 0x805b058c),
        Chunk(0x8059eaa4, 0x805a0558, 0x80594d80),
        Chunk(0x805a068c, 0x805a1478, 0x805b3ac8),
        Chunk(0x805a1488, 0x805a1864, 0x805b48b4),
        Chunk(0x805a1864, 0x805a9edc, 0x8059682c),
        Chunk(0x805a9edc, 0x805ab574, 0x8059eeac),
        Chunk(0x805ab574, 0x805abc90, 0x805a0604),
        Chunk(0x805abc90, 0x805add98, 0x805a0d28),
        Chunk(0x805add98, 0x805b9010, 0x805a2e70),
        Chunk(0x805b9010, 0x805b9300, 0x805b4c90),
        Chunk(0x805b9300, 0x805bab40, 0x8061f7f4),
        Chunk(0x805bab40, 0x805bb2b8, 0x805b4f80),
        Chunk(0x805bb2b8, 0x805bd2d8, 0x80621034),
        Chunk(0x805bd2d8, 0x805bd2e4, 0x805b695c),
        Chunk(0x805bd39c, 0x805be600, 0x805b56f8),
        Chunk(0x805be600, 0x805be604, 0x805b6968),
        Chunk(0x805be7f4, 0x805be84c, 0x805b76d0),
        Chunk(0x805be84c, 0x805bed68, 0x80623294),
        Chunk(0x805bed68, 0x805bed74, 0x805b7420),
        Chunk(0x805bed74, 0x805bf2d8, 0x806237b0),
        Chunk(0x805bf2d8, 0x805bf2dc, 0x805b919c),
        Chunk(0x805bf3cc, 0x805bfe1c, 0x805b69d0),
        Chunk(0x805bfe1c, 0x805c00c0, 0x805b742c),
        Chunk(0x805c00c0, 0x805c1b34, 0x805b7728),
        Chunk(0x805c1b34, 0x805c35f8, 0x805b91a0),
        Chunk(0x805c35f8, 0x805c3bcc, 0x80623e08),
        Chunk(0x805c3bcc, 0x805c4768, 0x805bac64),
        Chunk(0x805c4768, 0x805c579c, 0x806243dc),
        Chunk(0x805c57b0, 0x805caddc, 0x805bb800),
        Chunk(0x805caddc, 0x805cc0a8, 0x80625424),
        Chunk(0x805cc1b4, 0x805cd94c, 0x80626758),
        Chunk(0x805cd94c, 0x805d1888, 0x805c0e2c),
        Chunk(0x805d1888, 0x805d1e84, 0x80627ef0),
        Chunk(0x805d1e84, 0x805d7f78, 0x805c4d68),
        Chunk(0x805d7f78, 0x805dbfdc, 0x806284ec),
        Chunk(0x805dc034, 0x805de838, 0x8062c550),
        Chunk(0x805de844, 0x805e0c38, 0x8062ed54),
        Chunk(0x805e0c38, 0x805e6b50, 0x805cae5c),
        Chunk(0x805e6b50, 0x805e7460, 0x80631148),
        Chunk(0x805e7460, 0x805ea780, 0x805d0d74),
        Chunk(0x805ea780, 0x805eeb68, 0x80631a58),
        Chunk(0x805eeb68, 0x805f2d24, 0x805d4094),
        Chunk(0x805f2d24, 0x805f8b34, 0x80635e40),
        Chunk(0x805f8b34, 0x805fb5bc, 0x805d8250),
        Chunk(0x805fb5bc, 0x805fb820, 0x8063bc50),
        Chunk(0x805fb820, 0x805fd518, 0x805dacd8),
        Chunk(0x805fd518, 0x806012b0, 0x8063beb4),
        Chunk(0x806012b0, 0x80608d18, 0x805dc9d0),
        Chunk(0x80608d18, 0x8060a72c, 0x805e4444),
        Chunk(0x8060a72c, 0x8061186c, 0x8063fc4c),
        Chunk(0x8061186c, 0x80616844, 0x805e5e58),
        Chunk(0x80616844, 0x8061ae6c, 0x80646d8c),
        Chunk(0x8061ae6c, 0x8061e898, 0x805eae30),
        Chunk(0x8061e898, 0x8061f6e8, 0x8064b3b4),
        Chunk(0x8061f6e8, 0x80620cb4, 0x805ee85c),
        Chunk(0x80620d7c, 0x80634f48, 0x805efec8),
        Chunk(0x80634f48, 0x80637494, 0x806040b0),
        Chunk(0x80637514, 0x80637a30, 0x8064c204),
        Chunk(0x80637ac0, 0x8063bcf8, 0x80606720),
        Chunk(0x8063be40, 0x806453e4, 0x8060aa20),
        Chunk(0x806453e4, 0x806467d4, 0x8064c78c),
        Chunk(0x806467d4, 0x8064a3f4, 0x80613fc4),
        Chunk(0x8064a3f4, 0x8064aee4, 0x8064db7c),
        Chunk(0x8064aef8, 0x80651bec, 0x80617be4),
        Chunk(0x80651bec, 0x80652300, 0x8064e66c),
        Chunk(0x80652300, 0x80653208, 0x8061e8ec),
        Chunk(0x80653208, 0x8065b354, 0x8064ed80),
        Chunk(0x8065b4e8, 0x8065c0ec, 0x80656ecc),
        Chunk(0x8065c0ec, 0x8065fa14, 0x8065cd74),
        Chunk(0x8065fa4c, 0x8065fe4c, 0x80657ad0),
        Chunk(0x8065fe4c, 0x80662778, 0x80657f10),
        Chunk(0x80662778, 0x80663194, 0x80660694),
        Chunk(0x80663194, 0x80665538, 0x8065a83c),
        Chunk(0x80665538, 0x80668814, 0x80673188),
        Chunk(0x80668814, 0x8067906c, 0x806610b0),
        Chunk(0x8067906c, 0x80679380, 0x80676464),
        Chunk(0x80679380, 0x8067ac00, 0x80671908),
        Chunk(0x8067ac00, 0x806bf4c8, 0x80676778),
        Chunk(0x806bf4c8, 0x806bfb14, 0x806e20a8),
        Chunk(0x806bfb14, 0x806c050c, 0x806bb040),
        Chunk(0x806c050c, 0x806c35a8, 0x806e26f4),
        Chunk(0x806c35a8, 0x806c3aa4, 0x806bba38),
        Chunk(0x806c3aa4, 0x806c4ed4, 0x806e5790),
        Chunk(0x806c4ef0, 0x806c63a8, 0x806e6bc0),
        Chunk(0x806c63b0, 0x806c6b44, 0x806e8078),
        Chunk(0x806c6b44, 0x806cce90, 0x806bbf50),
        Chunk(0x806cce90, 0x806ce820, 0x806e880c),
        Chunk(0x806ce828, 0x806d02bc, 0x806c229c),
        Chunk(0x806d02bc, 0x806d28f4, 0x806ea19c),
        Chunk(0x806d2908, 0x806d5c5c, 0x806c3d38),
        Chunk(0x806d5c60, 0x806d5ed8, 0x806ec7d4),
        Chunk(0x806d5ed8, 0x806da914, 0x806c7098),
        Chunk(0x806da914, 0x806db184, 0x806eca58),
        Chunk(0x806db184, 0x806dda84, 0x806cbad4),
        Chunk(0x806dda84, 0x806deb40, 0x806ed2c8),
        Chunk(0x806deb40, 0x806df7d0, 0x806ce3d4),
        Chunk(0x806df7d0, 0x806dfd14, 0x806ee384),
        Chunk(0x806dfd14, 0x806e3a8c, 0x806cf064),
        Chunk(0x806e3a8c, 0x806e3e20, 0x806ee8c8),
        Chunk(0x806e3e20, 0x806e95b0, 0x806d2ddc),
        Chunk(0x806e95b0, 0x806ec7c0, 0x806eec5c),
        Chunk(0x806ec7c0, 0x806ed53c, 0x806d8564),
        Chunk(0x806ed53c, 0x806f62fc, 0x806d92e8),
        Chunk(0x806f62fc, 0x806f7698, 0x806f1e74),
        Chunk(0x806f77c4, 0x806f7a54, 0x80713a78),
        Chunk(0x806f7aa8, 0x806f8220, 0x80713d08),
        Chunk(0x806f8220, 0x806f8934, 0x806f3210),
        Chunk(0x806f8934, 0x806fa3fc, 0x806f3978),
        Chunk(0x806fa3fc, 0x806fe240, 0x806f5494),
        Chunk(0x806fe240, 0x806fe9e0, 0x806f9330),
        Chunk(0x806fe9e0, 0x807001a4, 0x80714480),
        Chunk(0x80700230, 0x80700474, 0x80715c44),
        Chunk(0x80700474, 0x8070e7b8, 0x806f9ad0),
        Chunk(0x8070e7b8, 0x8070f8b8, 0x80715e88),
        Chunk(0x8070f8b8, 0x807179c4, 0x80707e14),
        Chunk(0x807179c4, 0x80717e34, 0x8070ffac),
        Chunk(0x80717e34, 0x807182e8, 0x80716f88),
        Chunk(0x807182e8, 0x8071b86c, 0x8071041c),
        Chunk(0x8071b86c, 0x80726574, 0x8071743c),
        Chunk(0x80726574, 0x8072820c, 0x8073c5dc),
        Chunk(0x8072821c, 0x807285c8, 0x8073e274),
        Chunk(0x807285cc, 0x80729338, 0x8073e620),
        Chunk(0x80729350, 0x80729b88, 0x80722144),
        Chunk(0x80729b88, 0x8072a894, 0x80722984),
        Chunk(0x8072a894, 0x8072b95c, 0x80723698),
        Chunk(0x8072b95c, 0x8072de64, 0x80724770),
        Chunk(0x8072dfcc, 0x8072ff60, 0x8073f390),
        Chunk(0x8072ff78, 0x80730198, 0x80741324),
        Chunk(0x80730198, 0x80730a80, 0x80726de8),
        Chunk(0x80730b40, 0x80731960, 0x80741544),
        Chunk(0x80731960, 0x80735948, 0x807277a8),
        Chunk(0x80735948, 0x80738db8, 0x80742364),
        Chunk(0x80738db8, 0x8073c54c, 0x8072b790),
        Chunk(0x8073c54c, 0x8073edf0, 0x807457d4),
        Chunk(0x8073edf0, 0x8074c4a8, 0x8072ef24),
        Chunk(0x8074c4a8, 0x8074d5b8, 0x8076ceac),
        Chunk(0x8074d5b8, 0x807519c8, 0x80748078),
        Chunk(0x807519c8, 0x80754104, 0x8076dfbc),
        Chunk(0x80754104, 0x80758bdc, 0x8074c488),
        Chunk(0x80758bdc, 0x8075db24, 0x807706f8),
        Chunk(0x8075db3c, 0x8075e78c, 0x80750f60),
        Chunk(0x8075e78c, 0x8075eafc, 0x80775658),
        Chunk(0x8075eafc, 0x80765c94, 0x80751bb0),
        Chunk(0x80765c94, 0x807678f4, 0x807759c8),
        Chunk(0x807678f4, 0x80768d20, 0x80758d48),
        Chunk(0x80768d20, 0x807693ec, 0x80777628),
        Chunk(0x8076960c, 0x8076c85c, 0x80777e68),
        Chunk(0x8076c85c, 0x8076ebdc, 0x8075a174),
        Chunk(0x8076ebe0, 0x8076f2dc, 0x8077b0b8),
        Chunk(0x8076f2dc, 0x807726c4, 0x8075c4f4),
        Chunk(0x80772704, 0x80773c14, 0x8077b7b8),
        Chunk(0x80773c1c, 0x8077439c, 0x8075f8dc),
        Chunk(0x807743a0, 0x807787f0, 0x8076010c),
        Chunk(0x807787f0, 0x8077902c, 0x8077cd10),
        Chunk(0x8077902c, 0x8077ce88, 0x8076455c),
        Chunk(0x8077cec8, 0x8077df24, 0x8077d54c),
        Chunk(0x8077df24, 0x807829d8, 0x807683f8),
        Chunk(0x807829d8, 0x80787d84, 0x8077e5a8),
        Chunk(0x80787d84, 0x8078c960, 0x807d031c),
        Chunk(0x8078c960, 0x807a81b4, 0x80783954),
        Chunk(0x807a81b4, 0x807a9d70, 0x807d4f74),
        Chunk(0x807a9eb8, 0x807af140, 0x8079f210),
        Chunk(0x807af140, 0x807b2ef8, 0x807d6b94),
        Chunk(0x807b2ef8, 0x807d976c, 0x807a4498),
        Chunk(0x807d976c, 0x807d9b80, 0x807da94c),
        Chunk(0x807d9b98, 0x807da5c0, 0x807cad0c),
        Chunk(0x807da5c0, 0x807dbccc, 0x807dad78),
        Chunk(0x807dbccc, 0x807dc8c8, 0x807cb734),
        Chunk(0x807dc950, 0x807e093c, 0x807cc330),
        Chunk(0x807e093c, 0x807e2520, 0x8083c6f0),
        Chunk(0x807e259c, 0x807e5610, 0x807dc50c),
        Chunk(0x807e5654, 0x807e6414, 0x807df5e4),
        Chunk(0x807e6414, 0x807e9c44, 0x8083e33c),
        Chunk(0x807e9c50, 0x807edd98, 0x807e03a4),
        Chunk(0x807edd98, 0x807ee23c, 0x80841b6c),
        Chunk(0x807ee250, 0x807ee468, 0x807e44ec),
        Chunk(0x807ee474, 0x807eea14, 0x80842010),
        Chunk(0x807eea14, 0x807ef9f4, 0x807e4704),
        Chunk(0x807efd0c, 0x807f76ec, 0x807e56e4),
        Chunk(0x807f76ec, 0x807f7ba4, 0x808428e8),
        Chunk(0x807f7bc4, 0x807f890c, 0x807ed0c4),
        Chunk(0x807f8968, 0x807f9280, 0x80842da0),
        Chunk(0x807f9580, 0x807fab58, 0x808438a0),
        Chunk(0x807fab58, 0x807feb68, 0x807edf98),
        Chunk(0x807feb68, 0x807ffae0, 0x80844e78),
        Chunk(0x807ffb20, 0x80805a0c, 0x807f1fa8),
        Chunk(0x80805a0c, 0x8080761c, 0x80845df0),
        Chunk(0x8080761c, 0x80809448, 0x807f7ed4),
        Chunk(0x80809448, 0x8080ad20, 0x80847a00),
        Chunk(0x8080ad20, 0x80811e48, 0x807f9d00),
        Chunk(0x80811e48, 0x80813bd4, 0x808492d8),
        Chunk(0x80813bd4, 0x8081e284, 0x80800e28),
        Chunk(0x8081e284, 0x8081efec, 0x8084b064),
        Chunk(0x8081efec, 0x8082e540, 0x8080b4d8),
        Chunk(0x8082e540, 0x8082e854, 0x8084bdcc),
        Chunk(0x8082e854, 0x8082f408, 0x8081aa2c),
        Chunk(0x8082f408, 0x808334a0, 0x8084c0e0),
        Chunk(0x808334e0, 0x80833b00, 0x8081b5e0),
        Chunk(0x80833b00, 0x80838e4c, 0x8081bc08),
        Chunk(0x80838e60, 0x8083b0c0, 0x808501b8),
        Chunk(0x8083b0cc, 0x8083cb44, 0x80820f54),
        Chunk(0x8083cb44, 0x8083d42c, 0x80852424),
        Chunk(0x8083d42c, 0x80842334, 0x808229cc),
        Chunk(0x80842340, 0x808447ac, 0x80852d0c),
        Chunk(0x808447ac, 0x8084a9a0, 0x808278d4),
        Chunk(0x8084a9a0, 0x8084d0dc, 0x80855184),
        Chunk(0x8084d0dc, 0x80851d2c, 0x8082dac8),
        Chunk(0x80851d38, 0x80852c60, 0x808578c0),
        Chunk(0x80852c60, 0x80853ca4, 0x80832718),
        Chunk(0x80853ca4, 0x808551ec, 0x808587f4),
        Chunk(0x808551ec, 0x8085c3cc, 0x8083375c),
        Chunk(0x8085c3cc, 0x8085e674, 0x80859d3c),
        Chunk(0x8085e674, 0x8085f0ac, 0x8083a950),
        Chunk(0x8085f0ac, 0x8085ffd4, 0x8085bfe4),
        Chunk(0x8085ffd4, 0x80860f2c, 0x8083b388),
        Chunk(0x80860f2c, 0x80862e24, 0x8085cf0c),
        Chunk(0x80863234, 0x8086708c, 0x8085ee04),
        Chunk(0x8086708c, 0x808676e0, 0x80864d38),
        Chunk(0x808676e0, 0x808697bc, 0x80862c5c),
        Chunk(0x808697bc, 0x8086a254, 0x8086538c),
        Chunk(0x8086a254, 0x8086c098, 0x808766f4),
        Chunk(0x8086c108, 0x8086c988, 0x80878538),
        Chunk(0x8086ca40, 0x80872ca4, 0x80878db8),
        Chunk(0x80872ca4, 0x808739b0, 0x80865e24),
        Chunk(0x808739b0, 0x80875454, 0x80866be8),
        Chunk(0x80875454, 0x8088344c, 0x808686fc),
        Chunk(0x8088344c, 0x8088f400, 0x8087f01c),
        Chunk(0x808b3984, 0x808b3988, 0x808af134),
        Chunk(0x808b5b1c, 0x808b5b20, 0x808b125c),
        Chunk(0x808b5c78, 0x808b5c7c, 0x808b13b8),
        Chunk(0x808cb550, 0x808cb554, 0x808c6048),
        Chunk(0x808d3698, 0x808d369c, 0x808d5148),
        Chunk(0x808d36d4, 0x808d36d8, 0x808d5184),
        Chunk(0x808d374c, 0x808d3750, 0x808d51fc),
        Chunk(0x808da318, 0x808da368, 0x808d3f60),
        Chunk(0x809bd70c, 0x809bd710, 0x809b8f4c),
        Chunk(0x809bd728, 0x809bd72c, 0x809b8f68),
        Chunk(0x809bd730, 0x809bd734, 0x809b8f70),
        Chunk(0x809bd740, 0x809bd744, 0x809b8f80),
        Chunk(0x809bd748, 0x809bd74c, 0x809b8f88),
        Chunk(0x809c18f8, 0x809c18fc, 0x809bd110),
        Chunk(0x809c1e38, 0x809c1e3c, 0x809bd508),
        Chunk(0x809c2f38, 0x809c2f3c, 0x809be740),
        Chunk(0x809c38b8, 0x809c38bc, 0x809bf0b0),
        Chunk(0x809c4680, 0x809c4684, 0x809bfdc0),
    ],
    'J': [
        Chunk(0x80004000, 0x80008004, 0x80004000),
        Chunk(0x800080f4, 0x8000ac50, 0x80008050),
        Chunk(0x8000af78, 0x80021ba8, 0x8000ae9c),
        Chunk(0x80021bb0, 0x80244ea4, 0x80021ad0),
        Chunk(0x802a4080, 0x8038917c, 0x802a3a00),
        Chunk(0x805103b4, 0x805cc0a8, 0x8050fd34),
        Chunk(0x805cc1b4, 0x805fa33c, 0x805cba90),
        Chunk(0x805fa344, 0x805ff6e8, 0x805f9c20),
        Chunk(0x805ffd70, 0x806003e8, 0x805ff528),
        Chunk(0x80600c78, 0x80620cb4, 0x806003ec),
        Chunk(0x80620d7c, 0x80637a24, 0x806204c8),
        Chunk(0x80637a80, 0x8063bcf8, 0x8063716c),
        Chunk(0x8063be40, 0x8088f400, 0x8063b4ac),
        Chunk(0x808b3984, 0x808b3988, 0x808b2ae4),
        Chunk(0x808b5b1c, 0x808b5b20, 0x808b4c7c),
        Chunk(0x808b5c78, 0x808b5c7c, 0x808b4dd8),
        Chunk(0x808cb550, 0x808cb554, 0x808ca6a0),
        Chunk(0x808d3698, 0x808d369c, 0x808d27e8),
        Chunk(0x808d36d4, 0x808d36d8, 0x808d2824),
        Chunk(0x808d374c, 0x808d3750, 0x808d289c),
        Chunk(0x808da318, 0x808da368, 0x808d9468),
        Chunk(0x809bd70c, 0x809bd710, 0x809bc76c),
        Chunk(0x809bd728, 0x809bd72c, 0x809bc788),
        Chunk(0x809bd730, 0x809bd734, 0x809bc790),
        Chunk(0x809bd740, 0x809bd744, 0x809bc7a0),
        Chunk(0x809bd748, 0x809bd74c, 0x809bc7a8),
        Chunk(0x809c18f8, 0x809c18fc, 0x809c0958),
        Chunk(0x809c1e38, 0x809c1e3c, 0x809c0e98),
        Chunk(0x809c2f38, 0x809c2f3c, 0x809c1f98),
        Chunk(0x809c38b8, 0x809c38bc, 0x809c2918),
        Chunk(0x809c4680, 0x809c4684, 0x809c36e0),
    ],
    'K': [
        Chunk(0x80004000, 0x800074dc, 0x80004000),
        Chunk(0x800077c8, 0x800079d4, 0x80007894),
        Chunk(0x80007bc0, 0x80007bcc, 0x80007cac),
        Chunk(0x80007f2c, 0x80008004, 0x80008034),
        Chunk(0x80008c10, 0x80009198, 0x80008d60),
        Chunk(0x8000951c, 0x8000ac54, 0x80009624),
        Chunk(0x8000af78, 0x8000b610, 0x8000b024),
        Chunk(0x8000b654, 0x80021ba8, 0x8000b6bc),
        Chunk(0x80021bb0, 0x800ea264, 0x80021c10),
        Chunk(0x800ea4d4, 0x80164294, 0x800ea54c),
        Chunk(0x80164364, 0x801746fc, 0x80164400),
        Chunk(0x8017f680, 0x801e8414, 0x8017f9dc),
        Chunk(0x802100a0, 0x80244de0, 0x80210414),
        Chunk(0x802a4080, 0x803858e0, 0x80292080),
        Chunk(0x80385fc0, 0x8038917c, 0x80373fe0),
        Chunk(0x805103b4, 0x8051d72c, 0x804fe3d4),
        Chunk(0x8051e488, 0x8052a324, 0x8050c4ac),
        Chunk(0x8052a338, 0x805c08cc, 0x80518390),
        Chunk(0x805c08d4, 0x805cc0a8, 0x805ae938),
        Chunk(0x805cc220, 0x805ceae0, 0x805ba1e0),
        Chunk(0x805ceafc, 0x805cf0e8, 0x805bcabc),
        Chunk(0x805cf154, 0x805cf158, 0x805bd118),
        Chunk(0x805cf2bc, 0x805cf2c0, 0x805bd284),
        Chunk(0x805cf7e4, 0x805cf7e8, 0x805bd738),
        Chunk(0x805cf8bc, 0x805d00d0, 0x805bda40),
        Chunk(0x805d01c8, 0x805d124c, 0x805be350),
        Chunk(0x805d1260, 0x805eeb68, 0x805bf3fc),
        Chunk(0x805eeb68, 0x805fa33c, 0x805dcf88),
        Chunk(0x805fa344, 0x80620cb4, 0x805e8764),
        Chunk(0x80620d7c, 0x80637a24, 0x8060f174),
        Chunk(0x80637a80, 0x8063bcf8, 0x80625e18),
        Chunk(0x8063be40, 0x806681e8, 0x8062a158),
        Chunk(0x80668334, 0x80675464, 0x8065668c),
        Chunk(0x80675808, 0x80675eb8, 0x80663b68),
        Chunk(0x80675f2c, 0x806771f8, 0x8066428c),
        Chunk(0x80677c3c, 0x80678134, 0x80665fe4),
        Chunk(0x8067818c, 0x80742b58, 0x80666534),
        Chunk(0x80743154, 0x8088f400, 0x80731514),
        Chunk(0x808b3984, 0x808b3988, 0x808a1dfc),
        Chunk(0x808b5b1c, 0x808b5b20, 0x808a3f94),
        Chunk(0x808b5c78, 0x808b5c7c, 0x808a40f0),
        Chunk(0x808cb550, 0x808cb554, 0x808b99e8),
        Chunk(0x808d3698, 0x808d369c, 0x808c1b30),
        Chunk(0x808d36d4, 0x808d36d8, 0x808c1b6c),
        Chunk(0x808d374c, 0x808d3750, 0x808c1be4),
        Chunk(0x808da318, 0x808da368, 0x808c87b0),
        Chunk(0x809bd70c, 0x809bd710, 0x809abd4c),
        Chunk(0x809bd728, 0x809bd72c, 0x809abd68),
        Chunk(0x809bd730, 0x809bd734, 0x809abd70),
        Chunk(0x809bd740, 0x809bd744, 0x809abd80),
        Chunk(0x809bd748, 0x809bd74c, 0x809abd88),
        Chunk(0x809c18f8, 0x809c18fc, 0x809aff38),
        Chunk(0x809c1e38, 0x809c1e3c, 0x809b0478),
        Chunk(0x809c2f38, 0x809c2f3c, 0x809b1578),
        Chunk(0x809c38b8, 0x809c38bc, 0x809b13f8),
        Chunk(0x809c4680, 0x809c4684, 0x809b2cc0),
    ],
}


def write_symbol(out_file, name, address):
    out_file.write(f'    {name} = {address:#x};\n');

def get_binary_name(address):
    return next(name for name, src_binary in SRC_BINARIES.items() if address in src_binary)

def port(region, address):
    if region == 'P':
        return address

    return next((chunk.port(address) for chunk in CHUNKS[region] if address in chunk), None)


parser = ArgumentParser()
parser.add_argument('region')
parser.add_argument('in_path')
parser.add_argument('out_path')
args = parser.parse_args()

with open(args.out_path, 'w') as out_file:
    out_file.write('SECTIONS {\n')
    out_file.write('    .text base : { *(first) *(.text*) }\n')
    out_file.write('    patches : { *(patches*) }\n')
    out_file.write('    .rodata : { *(.rodata*) }\n')
    out_file.write('    .data : { *(.data*) *(.bss*) *(.sbss*) }\n')
    out_file.write('\n')

    for name, dst_binary in DST_BINARIES[args.region].items():
        write_symbol(out_file, f'{name}_start', dst_binary.start)
        write_symbol(out_file, f'{name}_end', dst_binary.end)
        out_file.write('\n')

    with open(args.in_path, 'r') as symbols:
        for symbol in symbols.readlines():
            if symbol.isspace():
                out_file.write('\n')
                continue
            address, name = symbol.split()
            address = int(address, 16)
            binary_name = get_binary_name(address)
            is_rel_bss = 0x809bd6e0 <= address < 0x809c4f90
            address = port(args.region, address)
            if address is None:
                sys.exit(f'Couldn\'t port symbol {name} to region {args.region}!')
            if is_rel_bss:
                address -= {
                    'P': 0xe02e0,
                    'E': 0xe0280,
                    'J': 0xe0200,
                    'K': 0xe04a0,
                }[args.region]
            address -= SRC_BINARIES[binary_name].start[args.region]
            address += DST_BINARIES[args.region][binary_name].start
            write_symbol(out_file, name, address)

    out_file.write('}\n')
