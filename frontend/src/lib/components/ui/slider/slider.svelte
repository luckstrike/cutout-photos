<script lang="ts">
	import { Slider as SliderPrimitive } from "bits-ui";
	import { cn, type WithoutChildrenOrChild } from "$lib/utils.js";

	let {
		ref = $bindable(null),
		value = $bindable(),
		orientation = "horizontal",
		class: className,
		...restProps
	}: WithoutChildrenOrChild<SliderPrimitive.RootProps> = $props();
</script>

<!--
Discriminated Unions + Destructing (required for bindable) do not
get along, so we shut typescript up by casting `value` to `never`.
-->
<SliderPrimitive.Root
	bind:ref
	bind:value={value as never}
	data-slot="slider"
	{orientation}
	class={cn(
		"relative mt-1 mb-4 flex w-full touch-none select-none items-center data-[orientation=vertical]:h-full data-[orientation=vertical]:min-h-44 data-[orientation=vertical]:w-auto data-[orientation=vertical]:flex-col data-[disabled]:opacity-50",
		className
	)}
	{...restProps}
>
	{#snippet children({ thumbs, tickItems })}
		<span
			data-orientation={orientation}
			data-slot="slider-track"
			class={cn(
				"bg-muted relative grow overflow-hidden rounded-full data-[orientation=horizontal]:h-1.5 data-[orientation=vertical]:h-full data-[orientation=horizontal]:w-full data-[orientation=vertical]:w-1.5"
			)}
		>
			<SliderPrimitive.Range
				data-slot="slider-range"
				class={cn(
					"bg-primary absolute data-[orientation=horizontal]:h-full data-[orientation=vertical]:w-full"
				)}
			/>
		</span>
		{#each thumbs as thumb (thumb)}
			<SliderPrimitive.Thumb
				data-slot="slider-thumb"
				index={thumb}
				class="border-primary bg-background ring-ring/50 focus-visible:outline-hidden block size-4 shrink-0 rounded-full border shadow-sm transition-[color,box-shadow] hover:ring-4 focus-visible:ring-4 disabled:pointer-events-none disabled:opacity-50"
			/>
		{/each}

		<!-- left end -->
		<SliderPrimitive.Tick index={0} />
		<SliderPrimitive.TickLabel 
			index={0}
			class="text-muted-foreground text-xs mt-2 mb-2"
			position="bottom"	
		>
			{tickItems[0].value}           <!-- real min value -->
		</SliderPrimitive.TickLabel>

		<!-- right end -->
		{@const last = tickItems.length - 1}
		<SliderPrimitive.Tick index={last} />
		<SliderPrimitive.TickLabel 
			index={last}
			class="text-muted-foreground text-xs mt-2 mb-2"
			position="bottom"
		>
			{tickItems[last].value}        <!-- real max value -->
		</SliderPrimitive.TickLabel>	

	{/snippet}
</SliderPrimitive.Root>
