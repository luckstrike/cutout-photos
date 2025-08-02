<script lang="ts">
    import CutoutOptions from "$lib/components/panels/cutoutOptions.svelte";
    import Navbar from "$lib/components/panels/navbar.svelte";
	import SelectImage from "$lib/components/panels/selectImage.svelte";

    import debounce from 'lodash.debounce';

    let debounceTiming: number = 300; // in ms

    let fileObj: File | null = $state(null);

    let outlineThickness : number = $state(0);
    let detailValue : number = $state(0);
    let outlineColor: string = $state("");

    function handleFileSelect(file: File | null) : void {
        if (!file) {
            return;
        }

        if (file.type.startsWith('image/')) {
            fileObj = file;
        }
    }

    function handleOutlineThicknessChange(thickness: number): void {
        outlineThickness = thickness;
    }

    function handleDetailValueChange(detail: number): void {
        detailValue = detail;
    }

    function handleOutlineColorChange(hexColor: string): void {
        outlineColor = hexColor;
    }


    $effect(() => {
        // TODO: When a file and options are selected, we can now process something!
        const createCutout = () => {
            /* 
             * 1. Reach out to REST API
             * 2. Get cutout image result back 
             * 3. Update the image shown by SelectImage
             */
        }

        const debouncedCutout = debounce(createCutout, debounceTiming);

        if (fileObj) {
            debouncedCutout();
        }

        return () => {
            debouncedCutout.cancel();
        };
    });
</script>

<div class="flex flex-col h-screen p-4 gap-4">
    <Navbar />
    <div class="flex flex-col items-center flex-1 gap-6">
        <h1 class="text-3xl font-semibold">Create a Cutout</h1>
        <div class="flex flex-col md:flex-row flex-1 max-w-4xl gap-8 p-2 items-center">
            <SelectImage {handleFileSelect}/>
            <CutoutOptions 
                {handleOutlineThicknessChange}
                {handleDetailValueChange}
                {handleOutlineColorChange}
            />
        </div>
    </div>
</div>