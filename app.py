import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./Registry/compiled/artregistry_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = "0x403F3B7CD42Cb38bD62f170361b96F3E32e8AD5e"

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()


st.title("Card Mint and Trading MVP")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address= st.selectbox("Select Account", options=accounts)
st.markdown("---")

################################################################################
# Register New Artwork
################################################################################
st.markdown("## Mint new Card")
artwork_name = st.text_input("Enter the name of the Card")
artist_name = st.text_input("Enter the artist name")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount in ETH")
artwork_uri = st.text_input("Enter the URI to the artwork")
if st.button("Mint Card"):
    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_name,
        artist_name,
        int(initial_appraisal_value),
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display Minted Cards")

selected_address = st.selectbox("Select Account to display", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} Cards")

token_id = st.selectbox("Artwork Cards Index Position", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The Card is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.write(f"The Card name is {artwork_name}")
    st.write(f"The Artist name is {artist_name}")
    st.write(f"The initial value in ETH is {initial_appraisal_value}")

    st.image(token_uri)
st.markdown("---")

################################################################################
# Trade Card
################################################################################
st.markdown('## Trade Cards')

from_address = st.selectbox("Select Account to trade from", options=accounts)
from_tokens = contract.functions.balanceOf(from_address).call()

st.write(f"The 'from' address owns {from_tokens} Cards")

fromToken_id = st.selectbox("Tradable Cards Index Position", list(range(from_tokens)))

to_address = st.selectbox("Select Account to trade to", options=accounts)
to_tokens = contract.functions.balanceOf(to_address).call()

st.write(f"The 'to' address owns {to_tokens} Cards")

if st.button("Trade Card"):

    trade_hash = contract.functions.safeTransferFrom(
        from_address,
        to_address,
        fromToken_id,
    ).transact({'from': from_address, 'to': to_address, 'tokenId': fromToken_id})
    receipt = w3.eth.waitForTransactionReceipt(trade_hash)
    st.write(receipt)

if st.button("Display Trade"):

    # Use the contract's `ownerOf` function to get the art token owner
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The Card is registered to {owner}")
st.markdown("---")
################################################################################
# Appraise Art
################################################################################
st.markdown("## Appraise Card")
tokens = contract.functions.totalSupply().call()
token_id = st.selectbox("Choose an Card Token ID", list(range(tokens)))
new_appraisal_value = st.text_input("Enter the new appraisal amount")
report_uri = st.text_area("Enter notes about the appraisal")
if st.button("Appraise Card"):

    # Use the token_id and the report_uri to record the appraisal
    tx_hash = contract.functions.newAppraisal(
        token_id,
        int(new_appraisal_value),
        report_uri
    ).transact({"from": w3.eth.accounts[0]})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(receipt)
st.markdown("---")

################################################################################
# Get Appraisals
################################################################################
st.markdown("## Get card appraisal report history")
art_token_id = st.number_input("Card ID", value=0, step=1)
if st.button("Get Appraisal Reports"):
    appraisal_filter = contract.events.Appraisal.createFilter(
        fromBlock=0,
        argument_filters={"tokenId": art_token_id}
    )
    appraisals = appraisal_filter.get_all_entries()
    if appraisals:
        for appraisal in appraisals:
            report_dictionary = dict(appraisal)
            st.markdown("### Appraisal Report Event Log")
            st.write(report_dictionary)
            st.markdown("### Appraisal Report Details")
            st.write(report_dictionary["args"])
    else:
        st.write("This Card has no new appraisals")
