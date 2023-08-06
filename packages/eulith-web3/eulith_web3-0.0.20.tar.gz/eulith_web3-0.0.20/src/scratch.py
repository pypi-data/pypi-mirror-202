from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.pendle import PendleClient

PENDLE_ROUTER = '0x0000000001e4ef00d069e71d6ba041b0a16f7ea0'
MARKET = '0x7D49E5Adc0EAAD9C027857767638613253eF125f'

if __name__ == '__main__':
    ew3 = EulithWeb3(eulith_url="https://arb-main.eulithrpc.com/v0",
                     eulith_refresh_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NksifQ."
                                          "eyJzdWIiOiJyYWNlciIsImV4cCI6MTcxMjk3Njg"
                                          "1MCwic291cmNlX2hhc2giOiIqIiwic2NvcGUiOi"
                                          "JBUElSZWZyZXNoIn0.VdFT4u_B-EIWZUnh_oormIf"
                                          "-rpp-NArOBrsfUjxLVPZOBO8h1ix8LhngfQFCiofk"
                                          "r5KkBtSoKTNcgBmR_iCH5hw")
    pc = PendleClient(ew3)

    quote = pc.quote_pt(10, ew3.to_checksum_address(MARKET))

    print(quote.price_denom_underlying)