<script>
	// @ts-nocheck

	let amount;
	let selectedToken;
</script>

<div class="fom-container">
	<h1 class="title mb-2">New RFQs</h1>
	<div class="rfq-form flex gap-2">
		<label class="label">
			<input class="input" type="text" placeholder="Amount In" bind:value={amount} />
		</label>
		<label class="label">
			<select bind:value={selectedToken} class="select">
				<option value="WETH">WETH</option>
				<option value="WBTC">WBTC</option>
				<option value="DAI">DAI</option>
				<option value="USDC">USDC</option>
			</select>
		</label>
		<button type="submit" class="btn-sm variant-ghost-surface">Submit</button>
	</div>
</div>

<style>
	.title {
		text-align: center;
		color: #30e9ff;
		text-transform: uppercase;
		letter-spacing: 2px;
		margin-bottom: 20px;
	}
	.fom-container {
		height: 100%;
		padding: 20px;
		border: 2px solid #30e9ff;
		border-radius: 10px;
		box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
	}
</style>
