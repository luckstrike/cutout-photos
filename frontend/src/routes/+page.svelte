<script lang="ts">
    import CutoutOptions from "$lib/components/panels/cutoutOptions.svelte";
    import Navbar from "$lib/components/panels/navbar.svelte";
	import SelectImage from "$lib/components/panels/selectImage.svelte";

    import debounce from 'lodash.debounce';
	import { onDestroy } from "svelte";

    const API_BASE : string = "http://127.0.0.1:8000"; // FastAPI server

    let debounceTiming : number = 300; // in ms

    let selectedFile : File | null = $state(null);
    let displayImageUrl : string | null = $state(null);
    let fileChanged : boolean = $state(false);
    
    let isLoading : boolean = $state(false);
    let processedCutout : boolean = $state(false);
    let error : string | null = $state(null);

    let outlineThickness : number = $state(50);
    let detailValue : number = $state(25);
    let outlineColor: string = $state("#0000FF");

    async function uploadData() {
        if (!selectedFile) {
            return;
        }

        processedCutout = false;
        isLoading = true;

        try {
            const formData = new FormData();

            formData.append('outline_thickness', outlineThickness.toString());
            formData.append('detail', detailValue.toString());
            formData.append('outline_color', outlineColor);
            formData.append('file', selectedFile);

            const response = await fetch(`${API_BASE}/api/upload`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const blob = await response.blob();

                if (displayImageUrl) {
                    URL.revokeObjectURL(displayImageUrl);
                }

                displayImageUrl = URL.createObjectURL(blob);
            }
        } catch (err : any) {
            error = 'Request failed: ' + err.message;
        } finally {
            isLoading = false;
            processedCutout = true;
        }

        return;
    }

    const debouncedProcess = debounce(() => {
        if (selectedFile) {
            uploadData();
        }
    }, debounceTiming);

    $effect(() => {
        if (selectedFile) {
            fileChanged = true;
        }
    })

    $effect(() => {
        if (selectedFile && outlineThickness && detailValue && outlineColor) {
            if (fileChanged) {
                if (displayImageUrl) {
                    URL.revokeObjectURL(displayImageUrl);
                }
                displayImageUrl = URL.createObjectURL(selectedFile);
                isLoading = false;
                fileChanged = false;

                debouncedProcess();
                
            } else {
                debouncedProcess();
            }

        }
    });

    onDestroy(() => {
        debouncedProcess.cancel();

        if (displayImageUrl) {
            URL.revokeObjectURL(displayImageUrl);
        }
    });
</script>

<div class="flex flex-col h-screen p-4 gap-4">
    <Navbar />
    <div class="flex flex-col items-center flex-1 gap-6">
        <h1 class="text-3xl font-semibold">Create a Cutout</h1>
        <div class="flex flex-col md:flex-row flex-1 max-w-4xl gap-8 p-2 items-center">
            <SelectImage bind:selectedFile={selectedFile} {displayImageUrl} {isLoading}/>
            <CutoutOptions
                bind:outlineThickness
                bind:detailValue
                bind:outlineColor
                {processedCutout}
            />
        </div>
    </div>
</div>