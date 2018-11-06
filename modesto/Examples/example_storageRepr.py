#!/usr/bin/env python
"""
Description
"""
import logging

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from pkg_resources import resource_filename

import modesto.utils as ut
from modesto.main import Modesto

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-36s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger('example_recomp')


def setup_graph(repr=False):
    G = nx.DiGraph()

    G.add_node('STC', x=0, y=0, z=0, comps={'solar': 'SolarThermalCollector',
                                            'backup': 'ProducerVariable'})
    G.add_node('demand', x=1000, y=100, z=0, comps={'build': 'BuildingFixed',
                                                    'stor': 'StorageRepr' if repr else 'StorageVariable'
                                                    })

    G.add_edge('STC', 'demand', name='pipe')

    return G


def setup_modesto(time_step=3600, n_steps=24 * 365, repr=False):
    repr_days = {
        4: {1: 74.0, 2: 307.0, 3: 307.0, 4: 307.0, 5: 307.0, 6: 307.0, 7: 307.0,
            8: 307.0, 9: 307.0, 10: 307.0,
            11: 307.0, 12: 307.0, 13: 307.0, 14: 307.0, 15: 307.0, 16: 307.0,
            17: 307.0, 18: 307.0, 19: 307.0,
            20: 307.0,
            21: 74.0, 22: 74.0, 23: 307.0, 24: 307.0, 25: 307.0, 26: 74.0,
            27: 74.0, 28: 307.0, 29: 307.0, 30: 307.0,
            31: 74.0, 32: 74.0, 33: 74.0, 34: 307.0, 35: 307.0, 36: 307.0,
            37: 307.0, 38: 307.0, 39: 307.0, 40: 307.0,
            41: 307.0, 42: 307.0, 43: 307.0, 44: 307.0, 45: 307.0, 46: 307.0,
            47: 307.0, 48: 307.0, 49: 307.0,
            50: 307.0,
            51: 307.0, 52: 74.0, 53: 295.0, 54: 307.0, 55: 74.0, 56: 307.0,
            57: 307.0, 58: 74.0, 59: 74.0, 60: 74.0,
            61: 74.0, 62: 307.0, 63: 307.0, 64: 307.0, 65: 74.0, 66: 307.0,
            67: 307.0, 68: 307.0, 69: 307.0, 70: 307.0,
            71: 307.0, 72: 74.0, 73: 307.0, 74: 74.0, 75: 295.0, 76: 295.0,
            77: 295.0, 78: 74.0, 79: 74.0, 80: 74.0,
            81: 74.0, 82: 74.0, 83: 74.0, 84: 74.0, 85: 74.0, 86: 74.0,
            87: 295.0, 88: 74.0, 89: 74.0, 90: 295.0,
            91: 307.0, 92: 74.0, 93: 307.0, 94: 295.0, 95: 248.0, 96: 248.0,
            97: 248.0, 98: 248.0, 99: 248.0,
            100: 248.0,
            101: 248.0, 102: 248.0, 103: 295.0, 104: 248.0, 105: 295.0,
            106: 74.0, 107: 248.0, 108: 248.0, 109: 307.0,
            110: 307.0, 111: 74.0, 112: 74.0, 113: 295.0, 114: 295.0, 115: 74.0,
            116: 74.0, 117: 74.0, 118: 74.0,
            119: 307.0, 120: 307.0, 121: 248.0, 122: 248.0, 123: 248.0,
            124: 248.0, 125: 248.0, 126: 248.0, 127: 248.0,
            128: 248.0, 129: 295.0, 130: 74.0, 131: 74.0, 132: 295.0,
            133: 248.0, 134: 295.0, 135: 295.0, 136: 248.0,
            137: 248.0, 138: 295.0, 139: 248.0, 140: 248.0, 141: 248.0,
            142: 248.0, 143: 248.0, 144: 248.0, 145: 248.0,
            146: 248.0, 147: 248.0, 148: 248.0, 149: 248.0, 150: 248.0,
            151: 248.0, 152: 248.0, 153: 248.0, 154: 248.0,
            155: 248.0, 156: 248.0, 157: 248.0, 158: 248.0, 159: 248.0,
            160: 295.0, 161: 248.0, 162: 248.0, 163: 248.0,
            164: 248.0, 165: 248.0, 166: 248.0, 167: 248.0, 168: 248.0,
            169: 248.0, 170: 248.0, 171: 248.0, 172: 248.0,
            173: 248.0, 174: 248.0, 175: 248.0, 176: 248.0, 177: 248.0,
            178: 248.0, 179: 248.0, 180: 248.0, 181: 248.0,
            182: 248.0, 183: 248.0, 184: 248.0, 185: 248.0, 186: 248.0,
            187: 248.0, 188: 248.0, 189: 248.0, 190: 248.0,
            191: 248.0, 192: 248.0, 193: 248.0, 194: 248.0, 195: 248.0,
            196: 248.0, 197: 248.0, 198: 248.0, 199: 248.0,
            200: 248.0, 201: 248.0, 202: 248.0, 203: 248.0, 204: 248.0,
            205: 248.0, 206: 248.0, 207: 248.0, 208: 248.0,
            209: 248.0, 210: 248.0, 211: 248.0, 212: 248.0, 213: 248.0,
            214: 248.0, 215: 248.0, 216: 248.0, 217: 248.0,
            218: 248.0, 219: 248.0, 220: 248.0, 221: 248.0, 222: 248.0,
            223: 248.0, 224: 248.0, 225: 248.0, 226: 248.0,
            227: 248.0, 228: 248.0, 229: 248.0, 230: 248.0, 231: 248.0,
            232: 248.0, 233: 248.0, 234: 248.0, 235: 248.0,
            236: 248.0, 237: 248.0, 238: 248.0, 239: 248.0, 240: 248.0,
            241: 248.0, 242: 248.0, 243: 248.0, 244: 248.0,
            245: 248.0, 246: 248.0, 247: 248.0, 248: 248.0, 249: 248.0,
            250: 248.0, 251: 248.0, 252: 248.0, 253: 295.0,
            254: 295.0, 255: 295.0, 256: 248.0, 257: 248.0, 258: 248.0,
            259: 248.0, 260: 248.0, 261: 248.0, 262: 248.0,
            263: 295.0, 264: 295.0, 265: 248.0, 266: 248.0, 267: 248.0,
            268: 248.0, 269: 248.0, 270: 248.0, 271: 295.0,
            272: 248.0, 273: 248.0, 274: 295.0, 275: 295.0, 276: 74.0,
            277: 74.0, 278: 295.0, 279: 295.0, 280: 295.0,
            281: 247.99999999579745, 282: 295.0, 283: 248.0, 284: 248.0,
            285: 248.0, 286: 248.0, 287: 248.0,
            288: 248.0,
            289: 295.0, 290: 295.0, 291: 295.0, 292: 295.0000000016577,
            293: 248.0, 294: 295.0, 295: 295.0, 296: 295.0,
            297: 74.0, 298: 74.0, 299: 307.0, 300: 74.0, 301: 307.0, 302: 74.0,
            303: 74.0, 304: 307.0, 305: 307.0,
            306: 307.0, 307: 307.0, 308: 307.0, 309: 307.0, 310: 307.0,
            311: 74.0, 312: 74.0, 313: 74.0, 314: 295.0,
            315: 295.0, 316: 295.0, 317: 74.0, 318: 74.0, 319: 307.0, 320: 74.0,
            321: 74.0, 322: 307.0, 323: 74.0,
            324: 295.0, 325: 307.0, 326: 307.0, 327: 307.0, 328: 307.0,
            329: 307.0, 330: 307.0, 331: 307.0, 332: 307.0,
            333: 307.0, 334: 307.0, 335: 307.0, 336: 307.0, 337: 307.0,
            338: 307.0, 339: 307.0, 340: 307.0, 341: 307.0,
            342: 307.0, 343: 307.0, 344: 307.0, 345: 307.0, 346: 307.0,
            347: 307.0, 348: 307.0, 349: 74.0, 350: 74.0,
            351: 307.0, 352: 74.0, 353: 74.0, 354: 74.0, 355: 307.0, 356: 307.0,
            357: 307.0, 358: 307.0, 359: 307.0,
            360: 307.0, 361: 307.0, 362: 307.0, 363: 307.0, 364: 74.0,
            365: 307.0},
        8: {1: 83.0, 2: 19.0, 3: 19.0, 4: 19.0, 5: 19.0, 6: 19.0, 7: 361.0,
            8: 361.0, 9: 361.0, 10: 361.0, 11: 361.0,
            12: 361.0, 13: 361.0, 14: 361.0, 15: 361.0, 16: 361.0, 17: 361.0,
            18: 19.0, 19: 19.0, 20: 19.0, 21: 83.0,
            22: 83.0, 23: 19.0, 24: 361.0, 25: 361.0, 26: 83.0, 27: 83.0,
            28: 19.0, 29: 19.0, 30: 19.0, 31: 83.0,
            32: 83.0, 33: 83.0, 34: 19.0, 35: 361.0, 36: 19.0, 37: 19.0,
            38: 19.0, 39: 361.0, 40: 361.0, 41: 19.0,
            42: 19.0, 43: 361.0, 44: 19.0, 45: 361.0, 46: 361.0, 47: 361.0,
            48: 19.0, 49: 361.0, 50: 19.0, 51: 19.0,
            52: 83.0, 53: 288.0, 54: 19.0, 55: 83.0, 56: 19.0, 57: 19.0,
            58: 83.0, 59: 83.0, 60: 83.0, 61: 83.0,
            62: 19.0, 63: 19.0, 64: 19.0, 65: 19.0, 66: 19.0, 67: 361.0,
            68: 19.0, 69: 19.0, 70: 19.0, 71: 19.0,
            72: 83.0, 73: 19.0, 74: 83.0, 75: 122.0, 76: 288.0, 77: 288.0,
            78: 288.0, 79: 83.0, 80: 83.0, 81: 288.0,
            82: 83.0, 83: 83.0, 84: 83.0, 85: 83.0, 86: 288.0, 87: 83.0,
            88: 83.0, 89: 83.0, 90: 288.0, 91: 19.0,
            92: 83.0, 93: 19.0, 94: 287.9999944769014, 95: 195.0,
            96: 195.00000107954747, 97: 195.0, 98: 195.0,
            99: 195.0, 100: 195.0, 101: 195.0, 102: 195.0, 103: 288.0,
            104: 195.0, 105: 195.00000110981634, 106: 288.0,
            107: 195.0, 108: 122.0, 109: 19.0, 110: 19.0, 111: 122.0, 112: 83.0,
            113: 83.0, 114: 122.0, 115: 83.0,
            116: 83.0, 117: 83.0, 118: 83.0, 119: 19.0, 120: 19.0, 121: 122.0,
            122: 122.0, 123: 122.0, 124: 288.0,
            125: 195.0, 126: 195.0, 127: 195.0, 128: 195.00000069135515,
            129: 288.0, 130: 83.0, 131: 288.0, 132: 195.0,
            133: 122.0, 134: 288.0, 135: 288.0, 136: 195.00000091008587,
            137: 122.0, 138: 288.0, 139: 122.0,
            140: 225.0, 141: 225.0, 142: 225.0, 143: 225.0, 144: 122.0,
            145: 209.0, 146: 225.0, 147: 225.0, 148: 225.0,
            149: 225.0, 150: 122.0, 151: 122.0, 152: 225.0, 153: 195.0,
            154: 195.0, 155: 122.0, 156: 122.0, 157: 195.0,
            158: 195.0, 159: 195.0, 160: 288.0, 161: 288.0, 162: 195.0,
            163: 225.0, 164: 225.0, 165: 225.0, 166: 225.0,
            167: 122.0, 168: 122.0, 169: 225.0, 170: 225.0, 171: 225.0,
            172: 209.0, 173: 225.0, 174: 225.0, 175: 209.0,
            176: 225.0, 177: 122.0, 178: 225.0, 179: 225.0, 180: 225.0,
            181: 195.0, 182: 195.0, 183: 195.0, 184: 209.0,
            185: 122.0, 186: 122.0, 187: 122.0, 188: 122.0, 189: 225.0,
            190: 225.0, 191: 225.0, 192: 209.0, 193: 209.0,
            194: 225.0, 195: 195.0, 196: 195.0, 197: 195.00000173206234,
            198: 195.0, 199: 225.0, 200: 225.0,
            201: 225.0, 202: 225.0, 203: 209.0, 204: 209.0, 205: 225.0,
            206: 225.0, 207: 225.0, 208: 209.0, 209: 209.0,
            210: 209.0, 211: 209.0, 212: 225.0, 213: 225.0, 214: 225.0,
            215: 122.0, 216: 195.0, 217: 122.0, 218: 122.0,
            219: 122.0, 220: 122.0, 221: 122.0, 222: 122.0, 223: 209.0,
            224: 225.0, 225: 225.0, 226: 225.0, 227: 209.0,
            228: 225.0, 229: 225.0, 230: 225.0, 231: 225.0, 232: 209.0,
            233: 225.0, 234: 225.0, 235: 195.0, 236: 225.0,
            237: 209.0, 238: 225.0, 239: 225.0, 240: 225.0, 241: 225.0,
            242: 225.0, 243: 225.0, 244: 225.0, 245: 225.0,
            246: 225.0, 247: 225.0, 248: 209.0, 249: 225.0, 250: 122.0,
            251: 195.0, 252: 195.0, 253: 288.0, 254: 288.0,
            255: 288.0, 256: 195.0, 257: 195.0, 258: 195.0, 259: 225.0,
            260: 195.0, 261: 195.0, 262: 288.0, 263: 288.0,
            264: 288.0, 265: 195.0, 266: 122.0, 267: 225.0, 268: 122.0,
            269: 122.0, 270: 122.0, 271: 288.0, 272: 122.0,
            273: 195.0, 274: 195.0, 275: 83.0, 276: 83.0, 277: 83.0, 278: 288.0,
            279: 288.0, 280: 288.0, 281: 288.0,
            282: 288.0, 283: 195.0, 284: 195.0, 285: 195.0, 286: 195.0,
            287: 195.0, 288: 288.0, 289: 288.0, 290: 288.0,
            291: 288.0, 292: 288.0, 293: 288.0, 294: 288.0, 295: 288.0,
            296: 83.0, 297: 83.0, 298: 83.0, 299: 19.0,
            300: 83.0, 301: 19.0, 302: 83.0, 303: 83.0, 304: 83.0, 305: 361.0,
            306: 19.0, 307: 19.0, 308: 19.0,
            309: 19.0, 310: 19.0, 311: 83.0, 312: 83.0, 313: 83.0, 314: 288.0,
            315: 288.0, 316: 83.0, 317: 83.0,
            318: 83.0, 319: 19.0, 320: 19.0, 321: 83.0, 322: 19.0, 323: 83.0,
            324: 83.0, 325: 19.0, 326: 19.0,
            327: 83.0, 328: 19.0, 329: 19.0, 330: 19.0, 331: 19.0, 332: 361.0,
            333: 361.0, 334: 361.0, 335: 361.0,
            336: 361.0, 337: 19.0, 338: 19.0, 339: 19.0, 340: 361.0, 341: 19.0,
            342: 19.0, 343: 361.0, 344: 19.0,
            345: 361.0, 346: 19.0, 347: 361.0, 348: 19.0, 349: 83.0, 350: 83.0,
            351: 19.0, 352: 83.0, 353: 83.0,
            354: 83.0, 355: 361.0, 356: 19.0, 357: 19.0, 358: 361.0, 359: 361.0,
            360: 361.0, 361: 361.0, 362: 361.0,
            363: 19.0, 364: 83.0, 365: 19.0},
        16: {1: 54.0, 2: 308.0, 3: 308.0, 4: 308.0, 5: 308.0, 6: 308.0,
             7: 308.0, 8: 361.0, 9: 361.0, 10: 361.0,
             11: 339.0, 12: 358.0, 13: 361.0, 14: 358.00000000665193, 15: 358.0,
             16: 361.0, 17: 361.0, 18: 308.0,
             19: 308.0, 20: 308.0, 21: 85.0, 22: 54.0, 23: 308.0, 24: 361.0,
             25: 308.0, 26: 308.0, 27: 85.0, 28: 308.0,
             29: 308.0, 30: 308.0, 31: 81.0, 32: 81.0, 33: 85.0, 34: 308.0,
             35: 361.0, 36: 308.0, 37: 308.0, 38: 308.0,
             39: 361.0, 40: 361.0, 41: 308.0, 42: 308.0, 43: 339.0,
             44: 308.0000000040243, 45: 358.0, 46: 361.0,
             47: 308.0, 48: 308.0, 49: 361.0, 50: 308.0, 51: 308.0, 52: 81.0,
             53: 81.0, 54: 54.0, 55: 111.0, 56: 308.0,
             57: 308.0, 58: 85.0, 59: 85.0, 60: 54.0, 61: 85.0, 62: 111.0,
             63: 308.0, 64: 308.0, 65: 308.0, 66: 308.0,
             67: 361.0, 68: 308.0, 69: 308.0, 70: 308.0, 71: 308.0, 72: 111.0,
             73: 308.0, 74: 85.0, 75: 111.0,
             76: 81.0, 77: 159.0, 78: 81.0, 79: 81.0, 80: 54.0, 81: 81.0,
             82: 85.0, 83: 85.0, 84: 85.0, 85: 85.0,
             86: 81.0, 87: 81.0, 88: 85.0, 89: 81.0, 90: 159.0, 91: 308.0,
             92: 111.0, 93: 308.0, 94: 111.0, 95: 285.0,
             96: 183.0, 97: 285.0, 98: 259.0, 99: 259.0, 100: 259.0, 101: 285.0,
             102: 159.0, 103: 80.99999998015326,
             104: 183.0, 105: 159.0, 106: 81.0, 107: 159.0, 108: 111.0,
             109: 308.0, 110: 308.0, 111: 111.0, 112: 81.0,
             113: 159.0, 114: 111.0, 115: 81.0, 116: 111.0,
             117: 81.00000000774045, 118: 111.0, 119: 308.0, 120: 308.0,
             121: 111.0, 122: 111.0, 123: 259.0, 124: 159.0, 125: 285.0,
             126: 285.0, 127: 159.0000000000686,
             128: 259.0, 129: 159.0, 130: 85.0, 131: 81.0, 132: 159.0,
             133: 111.0, 134: 159.0, 135: 159.0, 136: 183.0,
             137: 111.0, 138: 159.0, 139: 259.0, 140: 147.0, 141: 147.0,
             142: 166.0, 143: 166.0, 144: 259.0,
             145: 259.0, 146: 166.0, 147: 147.0, 148: 147.0, 149: 166.0,
             150: 186.0, 151: 259.0, 152: 166.0,
             153: 259.0, 154: 183.0, 155: 259.0, 156: 259.0, 157: 166.0,
             158: 259.0, 159: 159.0, 160: 159.0,
             161: 183.0, 162: 285.0, 163: 166.0, 164: 147.0, 165: 166.0,
             166: 166.0, 167: 183.0, 168: 186.0,
             169: 147.0, 170: 147.0, 171: 147.0, 172: 147.0, 173: 147.0,
             174: 174.0, 175: 174.0, 176: 147.0,
             177: 259.0, 178: 166.0, 179: 259.0, 180: 166.0, 181: 166.0,
             182: 284.999999981291, 183: 183.0, 184: 259.0,
             185: 186.0, 186: 186.0, 187: 111.0, 188: 183.0, 189: 166.0,
             190: 147.0, 191: 147.0, 192: 186.0,
             193: 259.0, 194: 166.0, 195: 183.0, 196: 183.0, 197: 183.0,
             198: 285.0, 199: 147.0, 200: 147.0,
             201: 166.0, 202: 147.0, 203: 147.0, 204: 174.0, 205: 147.0,
             206: 147.0, 207: 166.0, 208: 147.0,
             209: 174.0, 210: 174.0, 211: 147.0, 212: 147.0, 213: 147.0,
             214: 166.0, 215: 186.0, 216: 183.0,
             217: 183.0, 218: 186.0, 219: 111.0, 220: 186.0, 221: 183.0,
             222: 186.0, 223: 174.0, 224: 147.0,
             225: 166.0, 226: 147.0, 227: 174.0, 228: 147.0, 229: 147.0,
             230: 147.0, 231: 147.0, 232: 174.0,
             233: 147.0, 234: 166.0, 235: 166.0, 236: 166.0, 237: 147.0,
             238: 147.0, 239: 147.0, 240: 147.0,
             241: 147.0, 242: 147.0, 243: 147.0, 244: 147.0, 245: 147.0,
             246: 147.0, 247: 147.0, 248: 174.0,
             249: 166.0, 250: 182.99999998505461, 251: 285.0, 252: 285.0,
             253: 159.0, 254: 159.0,
             255: 158.99999999946374, 256: 285.0, 257: 285.0, 258: 285.0,
             259: 259.0, 260: 285.0, 261: 183.0,
             262: 183.0, 263: 159.0, 264: 159.0, 265: 183.0, 266: 259.0,
             267: 166.0, 268: 259.0, 269: 183.0,
             270: 183.0, 271: 183.0, 272: 111.0, 273: 259.0, 274: 159.0,
             275: 85.0, 276: 81.0, 277: 81.0, 278: 159.0,
             279: 183.0, 280: 158.99999996019196, 281: 159.0,
             282: 159.0000000861355, 283: 285.0, 284: 285.0,
             285: 285.0, 286: 259.0, 287: 259.0, 288: 183.0, 289: 159.0,
             290: 159.0, 291: 159.0, 292: 81.0, 293: 183.0,
             294: 183.0, 295: 159.0, 296: 111.0, 297: 81.0, 298: 85.0,
             299: 308.0, 300: 54.0, 301: 308.0, 302: 85.0,
             303: 85.0, 304: 54.0, 305: 339.0, 306: 308.0, 307: 308.0,
             308: 308.0, 309: 308.0, 310: 308.0, 311: 111.0,
             312: 54.0, 313: 81.0, 314: 159.0, 315: 158.99999999965095,
             316: 85.0, 317: 54.0, 318: 85.0, 319: 308.0,
             320: 308.0, 321: 54.0, 322: 308.0, 323: 81.0, 324: 54.0,
             325: 308.0, 326: 308.0, 327: 54.0, 328: 308.0,
             329: 308.0, 330: 308.0, 331: 308.0, 332: 339.0, 333: 339.0,
             334: 361.0, 335: 308.0, 336: 361.0,
             337: 308.0, 338: 308.0, 339: 339.0, 340: 361.0, 341: 308.0,
             342: 308.0, 343: 361.0, 344: 308.0,
             345: 361.0, 346: 308.0, 347: 339.0, 348: 308.0, 349: 54.0,
             350: 85.0, 351: 308.0, 352: 81.0, 353: 54.0,
             354: 54.0, 355: 360.9999999932424, 356: 308.0, 357: 308.0,
             358: 358.0, 359: 361.0, 360: 361.0, 361: 361.0,
             362: 361.0, 363: 308.0, 364: 308.0, 365: 307.999999997669},
        32: {1: 21.0, 2: 2.0, 3: 304.0, 4: 2.0, 5: 30.0, 6: 2.0, 7: 338.0,
             8: 338.0, 9: 9.0, 10: 9.0, 11: 338.0,
             12: 12.0, 13: 360.0, 14: 14.0, 15: 12.0, 16: 360.0, 17: 338.0,
             18: 356.0, 19: 30.0, 20: 30.0, 21: 21.0,
             22: 21.0, 23: 2.0, 24: 9.0, 25: 356.0, 26: 55.0, 27: 112.0,
             28: 2.0, 29: 55.0, 30: 30.0, 31: 112.0,
             32: 112.0, 33: 112.0, 34: 55.0, 35: 338.0, 36: 2.0, 37: 2.0,
             38: 55.0, 39: 342.0, 40: 8.999999942276366,
             41: 338.0, 42: 338.0, 43: 338.0, 44: 44.0, 45: 12.0, 46: 360.0,
             47: 338.0, 48: 304.0, 49: 338.0, 50: 55.0,
             51: 55.0, 52: 112.0, 53: 112.0, 54: 304.0, 55: 55.0, 56: 30.0,
             57: 2.0, 58: 112.0, 59: 84.0, 60: 55.0,
             61: 55.0, 62: 92.0, 63: 2.0, 64: 2.0, 65: 55.0, 66: 30.0,
             67: 338.0, 68: 356.0, 69: 2.0, 70: 2.0, 71: 2.0,
             72: 92.0, 73: 304.0, 74: 112.0, 75: 92.0, 76: 290.0, 77: 290.0,
             78: 78.0, 79: 112.0, 80: 21.0, 81: 112.0,
             82: 84.0, 83: 84.0, 84: 84.0, 85: 112.0, 86: 94.0, 87: 94.0,
             88: 112.0, 89: 112.0, 90: 290.0, 91: 304.0,
             92: 92.0, 93: 92.0, 94: 94.0, 95: 281.0, 96: 281.0, 97: 182.0,
             98: 207.0, 99: 207.0, 100: 207.0,
             101: 182.0, 102: 281.0, 103: 112.0, 104: 281.0, 105: 133.0,
             106: 94.0, 107: 133.0, 108: 133.0, 109: 30.0,
             110: 30.0, 111: 92.0, 112: 112.0, 113: 113.0, 114: 92.0, 115: 94.0,
             116: 133.0, 117: 112.0, 118: 92.0,
             119: 2.0, 120: 55.0, 121: 133.0, 122: 150.0, 123: 133.0, 124: 94.0,
             125: 281.0, 126: 182.0, 127: 281.0,
             128: 78.0, 129: 113.0, 130: 84.0, 131: 94.0, 132: 92.0, 133: 133.0,
             134: 94.0, 135: 290.0, 136: 281.0,
             137: 133.0, 138: 290.0, 139: 133.0, 140: 170.0, 141: 205.0,
             142: 207.0, 143: 207.0, 144: 210.0,
             145: 221.0, 146: 206.0, 147: 205.0, 148: 170.0, 149: 207.0,
             150: 150.0, 151: 210.0, 152: 207.0,
             153: 207.0, 154: 281.0, 155: 133.0, 156: 133.0, 157: 207.0,
             158: 281.0, 159: 133.0, 160: 290.0,
             161: 290.0, 162: 281.0, 163: 206.0, 164: 206.0, 165: 206.0,
             166: 206.0, 167: 221.0, 168: 150.0,
             169: 206.0, 170: 170.0, 171: 170.0, 172: 210.0, 173: 170.0,
             174: 205.0, 175: 210.0, 176: 170.0,
             177: 210.0, 178: 206.0, 179: 206.0, 180: 207.0, 181: 207.0,
             182: 182.0, 183: 182.0, 184: 221.0,
             185: 210.0, 186: 150.0, 187: 133.0, 188: 133.0, 189: 205.0,
             190: 170.0, 191: 205.0, 192: 210.0,
             193: 210.0, 194: 207.0, 195: 182.0, 196: 281.0, 197: 281.0,
             198: 182.0, 199: 205.0, 200: 205.0,
             201: 206.0, 202: 170.0, 203: 210.0, 204: 210.0, 205: 205.0,
             206: 206.0, 207: 207.0, 208: 206.0,
             209: 210.0, 210: 210.0, 211: 210.0, 212: 205.0, 213: 206.0,
             214: 206.0, 215: 150.0, 216: 281.0,
             217: 221.0, 218: 150.0, 219: 150.0, 220: 210.0, 221: 221.0,
             222: 210.0, 223: 210.0, 224: 205.0,
             225: 206.0, 226: 170.0, 227: 210.0, 228: 206.0, 229: 170.0,
             230: 170.0, 231: 170.0, 232: 210.0,
             233: 205.0, 234: 206.0, 235: 182.0, 236: 206.0, 237: 170.0,
             238: 205.0, 239: 170.0, 240: 170.0,
             241: 205.0, 242: 170.0, 243: 170.0, 244: 206.0, 245: 205.0,
             246: 205.0, 247: 170.0, 248: 210.0,
             249: 207.0, 250: 133.0, 251: 281.0, 252: 281.0, 253: 289.0,
             254: 94.0, 255: 94.0, 256: 78.0, 257: 182.0,
             258: 182.0, 259: 207.0, 260: 281.0, 261: 281.0, 262: 289.0,
             263: 290.0, 264: 290.0, 265: 281.0,
             266: 210.0, 267: 207.0, 268: 221.0, 269: 150.0, 270: 133.0,
             271: 94.0, 272: 133.0, 273: 281.0, 274: 78.0,
             275: 113.0, 276: 112.0, 277: 112.0, 278: 94.0, 279: 289.0,
             280: 290.0, 281: 281.0, 282: 290.0, 283: 182.0,
             284: 182.0, 285: 207.0, 286: 221.0, 287: 221.0, 288: 281.0,
             289: 289.0, 290: 290.0, 291: 94.0, 292: 94.0,
             293: 290.0, 294: 290.0, 295: 94.0, 296: 133.0, 297: 84.0,
             298: 84.0, 299: 304.0, 300: 55.0, 301: 2.0,
             302: 21.0, 303: 84.0, 304: 304.0, 305: 338.0, 306: 356.0, 307: 2.0,
             308: 2.0, 309: 30.0, 310: 30.0,
             311: 55.0, 312: 21.0, 313: 112.0, 314: 94.0, 315: 290.0,
             316: 113.0, 317: 21.0, 318: 21.0, 319: 30.0,
             320: 55.0, 321: 84.0, 322: 304.0, 323: 21.0, 324: 113.0,
             325: 304.0, 326: 55.0, 327: 21.0, 328: 2.0,
             329: 55.0, 330: 304.0, 331: 2.0, 332: 338.0, 333: 338.0,
             334: 342.0, 335: 338.0, 336: 9.0, 337: 55.0,
             338: 338.0, 339: 338.0, 340: 338.0, 341: 356.0, 342: 342.0,
             343: 338.0, 344: 344.0, 345: 9.0, 346: 356.0,
             347: 338.0, 348: 55.0, 349: 21.0, 350: 21.0, 351: 304.0, 352: 21.0,
             353: 84.0, 354: 21.0, 355: 338.0,
             356: 356.0, 357: 2.0, 358: 14.0, 359: 360.0000000556279,
             360: 360.0, 361: 9.000000000496122, 362: 360.0,
             363: 30.0, 364: 55.0, 365: 2.0}
    }

    model = Modesto(pipe_model='ExtensivePipe', graph=setup_graph(repr),
                    repr_days=repr_days[32] if repr else None)
    heat_demand = ut.read_time_data(
        resource_filename('modesto', 'Data/HeatDemand'),
        name='HeatDemandFiltered.csv')
    weather_data = ut.read_time_data(
        resource_filename('modesto', 'Data/Weather'), name='weatherData.csv')

    model.opt_settings(allow_flow_reversal=False)

    elec_cost = \
        ut.read_time_data(
            resource_filename('modesto', 'Data/ElectricityPrices'),
            name='DAM_electricity_prices-2014_BE.csv')['price_BE']

    general_params = {'Te': weather_data['Te'],
                      'Tg': weather_data['Tg'],
                      'Q_sol_E': weather_data['QsolE'],
                      'Q_sol_W': weather_data['QsolW'],
                      'Q_sol_S': weather_data['QsolS'],
                      'Q_sol_N': weather_data['QsolN'],
                      'time_step': time_step,
                      'horizon': n_steps * time_step,
                      'elec_cost': pd.Series(0.1, index=weather_data.index)}

    model.change_params(general_params)

    build_params = {
        'delta_T': 20,
        'mult': 1,
        'heat_profile': heat_demand['ZwartbergNEast']
    }
    model.change_params(build_params, node='demand', comp='build')

    stor_params = {
        'Thi': 80 + 273.15,
        'Tlo': 60 + 273.15,
        'mflo_max': 110,
        'mflo_min': -110,
        'mult': 1,
        'volume': 30000,
        'ar': 1,
        'dIns': 0.3,
        'kIns': 0.024,
        'heat_stor': 200000,
        'mflo_use': pd.Series(0, index=weather_data.index)
    }
    model.change_params(dict=stor_params, node='demand', comp='stor')
    model.change_init_type('heat_stor', new_type='cyclic', comp='stor',
                           node='demand')

    sol_data = ut.read_time_data(resource_filename(
        'modesto', 'Data/RenewableProduction'), name='SolarThermal.csv')['0_40']

    stc_params = {
        'delta_T': 20,
        'heat_profile': sol_data,
        'area': 2000
    }
    model.change_params(stc_params, node='STC', comp='solar')

    pipe_data = {
        'diameter': 250,
        'temperature_supply': 80 + 273.15,
        'temperature_return': 60 + 273.15
    }
    model.change_params(pipe_data, node=None, comp='pipe')

    backup_params = {
        'delta_T': 20,
        'efficiency': 0.95,
        'PEF': 1,
        'CO2': 0.178,
        'fuel_cost': elec_cost,
        'Qmax': 10e6,
        'ramp_cost': 0,
        'ramp': 0
    }
    model.change_params(backup_params, node='STC', comp='backup')

    return model


if __name__ == '__main__':
    t_step = 3600
    n_steps = 24 * 365
    start_time = pd.Timestamp('20140101')

    optmodel_full = setup_modesto(t_step, n_steps, repr=False)
    optmodel_repr = setup_modesto(t_step, n_steps, repr=True)

    optmodel_full.compile(start_time)
    assert optmodel_full.compiled, 'optmodel_full should have a flag compiled=True'

    optmodel_full.change_param(node='STC', comp='solar', param='area', val=40000)
    optmodel_full.compile(start_time=start_time)

    optmodel_repr.change_param(node='STC', comp='solar', param='area', val=40000)
    optmodel_repr.compile(start_time=start_time, recompile=True)

    optmodel_repr.set_objective('cost')
    optmodel_full.set_objective('cost')

    sol_m = optmodel_full.solve(tee=True)
    sol_r = optmodel_repr.solve(tee=True)

    h_sol_repr = optmodel_repr.get_result('heat_flow', node='STC', comp='solar')
    h_sol_full = optmodel_full.get_result('heat_flow', node='STC', comp='solar')

    q_dem_repr = optmodel_repr.get_result('heat_flow', node='demand',
                                         comp='build')
    q_dem_full = optmodel_full.get_result('heat_flow', node='demand',
                                         comp='build')

    q_stor_repr = optmodel_repr.get_result('heat_flow', node='demand',
                                          comp='stor')
    q_stor_full = optmodel_full.get_result('heat_flow', node='demand',
                                          comp='stor')

    q_repr = optmodel_repr.get_result('heat_flow', node='STC', comp='backup')
    q_full = optmodel_full.get_result('heat_flow', node='STC', comp='backup')

    soc_repr = optmodel_repr.get_result('heat_stor', node='demand', comp='stor')
    soc_full = optmodel_full.get_result('heat_stor', node='demand', comp='stor')

    soc_inter = optmodel_repr.get_result('heat_stor_inter', node='demand',
                                         comp='stor')
    soc_intra = optmodel_repr.get_result('heat_stor_intra', node='demand',
                                         comp='stor')

    print h_sol_full.equals(h_sol_repr)
    print 'Mutable object'
    print optmodel_full.components['STC.solar'].block.area.value

    print 'Recompiled object'
    print optmodel_repr.components['STC.solar'].block.area.value

    plt.style.use('ggplot')
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(h_sol_repr, '-', label='Sol repr', color='r')
    ax[0].plot(h_sol_full, '--', label='Sol full', color='r')

    ax[0].plot(q_stor_repr, '-', label='Storage q repr', color='b')
    ax[0].plot(q_stor_full, '--', label='Storage q full', color='b')

    ax[0].plot(q_repr, label='Prod repr', color='y')
    ax[0].plot(q_full, '--', label='Prod full', color='y')

    ax[0].plot(q_dem_repr, label='Demand repr', color='k')
    ax[0].plot(q_dem_full, '--', label='Demand full', color='k')

    ax[1].plot(soc_repr, label='SOC repr')
    ax[1].plot(soc_full, '--', label='SOC full')

    ax[1].plot(soc_inter, '*')
    ax[1].plot(soc_intra, ':')

    ax[1].legend()

    fig.savefig('ReprStorage.png', dpi=600, figsize=(16,12), bbox_inches='tight')

    ax[0].legend()

    plt.show()
