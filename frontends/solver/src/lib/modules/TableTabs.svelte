<script>
	import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
	import TableComponent from '$lib/components/TableComponent.svelte';
	let tabSet = 0;
</script>

<TabGroup>
	<Tab bind:group={tabSet} name="tab1" value={0}>
		<span>RFQs</span>
	</Tab>
	<Tab bind:group={tabSet} name="tab2" value={1}>Finalized Trades</Tab>
	<!-- Tab Panels --->
	<svelte:fragment slot="panel">
		{#if tabSet === 0}
			<TableComponent />
		{:else if tabSet === 1}
			<TableComponent />
		{/if}
	</svelte:fragment>
</TabGroup>
