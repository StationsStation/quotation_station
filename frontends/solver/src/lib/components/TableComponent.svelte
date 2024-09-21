<script>
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
	import { rfqData } from '../mock';

	const tableSimple = {
		// A list of heading labels.
		head: ['AMOUNT IN', 'ASK', 'BID', 'BUYER', 'CHAIN', 'EXPIRATION'],
		// The data visibly shown in your table body UI.
		body: tableMapperValues(rfqData, [
			'amount_in',
			'ask_token_id',
			'bid_token_id',
			'buyer_wallet_address',
			'chain_id',
			'expiration_time'
		])
	};
</script>

<Table source={tableSimple} />
