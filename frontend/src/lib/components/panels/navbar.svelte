<script lang="ts">
    import ModeToggle from "$lib/components/ui/modeToggle/modeToggle.svelte";
	import Button from "../ui/button/button.svelte";
</script>

<div class="flex justify-end space-x-2">
    <Button variant="outline" href="/">Home</Button>
    <ModeToggle />
</div>