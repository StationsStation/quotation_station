<script>
	const GRAFANA_URL = '';
	let url = '';
	$: inputUrl = url;
</script>

<div class="frame">
	<input type="text" placeholder="Enter your grafana url" bind:value={url} />
	<div class="container">
		<iframe
			title="dashboard"
			src={inputUrl || GRAFANA_URL}
			width="100%"
			height="100%"
			frameborder="0"
		/>
	</div>
</div>

<style>
	.frame {
		height: 100%;
	}
	.container {
		margin-top: 10px;
		max-height: 500px;
		height: 100%;
	}
	input {
		border-radius: 5px;
		padding: 3px;
		width: 100%;
		background: rgb(17, 17, 20);
		color: white;
		margin-top: 5px;
		margin-left: 5px;
		border: 0.8px solid #258dc9b7;
	}
</style>
