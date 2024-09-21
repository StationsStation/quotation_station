<script>
	let price = '123';
	const PRICE_URL = 'http://localhost:5556';

	function getPrice() {}
</script>

<div class="section-container">
	<h1>Best Price</h1>
	<div class="flex">
		<input type="text" bind:value={price} placeholder="Best Price" style="width: 100%;" disabled />
	</div>
</div>

<style>
	input {
		margin-bottom: 10px;
		padding: 5px;
		background-color: black;
		border-radius: 4px;
	}
	button {
		padding: 5px 10px;
		cursor: pointer;
		height: 35px;
	}
	h1 {
		text-align: center;
		color: #30e9ff;
		text-transform: uppercase;
		letter-spacing: 2px;
		margin-bottom: 20px;
	}
	.section-container {
		padding: 22px;
		border: 2px solid #30e9ff;
		border-radius: 10px;
		box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
	}
</style>
