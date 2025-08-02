<script lang="ts">
    import CutoutOptions from "$lib/components/panels/cutoutOptions.svelte";
    import Navbar from "$lib/components/panels/navbar.svelte";
	import SelectImage from "$lib/components/panels/selectImage.svelte";

    import debounce from 'lodash.debounce';
	import { onDestroy } from "svelte";

    const API_BASE = "http://127.0.0.1:8000"; // FastAPI server

    let debounceTiming: number = 300; // in ms

    let fileObj: File | null = $state(null);
    
    let isLoading : boolean = $state(false);
    let imageUrl : string | null = $state(null);
    let error : string | null = $state(null);

    let outlineThickness : number = $state(0);
    let detailValue : number = $state(0);
    let outlineColor: string = $state("");

    function cleanUpImageUrl(): void {
        if (imageUrl) {
            URL.revokeObjectURL(imageUrl);
            imageUrl = null;
        }
    }
    
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

    async function uploadData() {
        if (!fileObj) {
            return;
        }

        try {
            const formData = new FormData();

            formData.append('outline_thickness', outlineThickness.toString());
            formData.append('detail', detailValue.toString());
            formData.append('outline_color', outlineColor);

            formData.append('file', fileObj);

            const response = await fetch(`${API_BASE}/api/upload`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const blob = await response.blob();

                cleanUpImageUrl();

                imageUrl = URL.createObjectURL(blob);
                
                // Get metadata from headers if you added them
                const fileSize = response.headers.get('X-File-Size');

                return imageUrl;
            } else {
                // Error responses might still be JSON
                try {
                    const errorData = await response.json();
                    error = errorData.detail || 'Upload failed';
                } catch {
                    // If error response isn't JSON either
                    error = `HTTP ${response.status}: ${response.statusText}`;
                }
            }

        } catch (err : any) {
            error = 'Request failed: ' + err.message;
        } finally {
            isLoading = false;
        }

        return;
    }

    $effect(() => {
        const createCutout = () => {
            const result = uploadData();
        }

        const debouncedCutout = debounce(createCutout, debounceTiming);

        if (fileObj) {
            debouncedCutout();
        }

        return () => {
            debouncedCutout.cancel();
        };
    });

    onDestroy(() => {
        cleanUpImageUrl();
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