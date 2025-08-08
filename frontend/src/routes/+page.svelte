<script lang="ts">
  import CutoutOptions from "$lib/components/panels/cutoutOptions.svelte";
  import Navbar from "$lib/components/panels/navbar.svelte";
  import SelectImage from "$lib/components/panels/selectImage.svelte";
  import debounce from "lodash.debounce";
  import { onDestroy } from "svelte";

  const API_BASE: string = "http://127.0.0.1:8000";

  let debounceTiming: number = 300;

  let selectedFile: File | null = $state(null);
  let displayImageUrl: string | null = $state(null);
  let fileChanged: boolean = $state(false);

  let isLoading: boolean = $state(false);
  let processedCutout: boolean = $state(false);
  let error: string | null = $state(null);

  let outlineThickness: number = $state(50);
  let detailValue: number = $state(25);
  let outlineColor: string = $state("#0000FF");

  // NEW: keep the server-suggested filename
  let suggestedFilename: string = $state("cutout.png");

  async function uploadData() {
    if (!selectedFile) return;

    processedCutout = false;
    isLoading = true;

    try {
      const formData = new FormData();
      formData.append("outline_thickness", outlineThickness.toString());
      formData.append("detail", detailValue.toString());
      formData.append("outline_color", outlineColor);
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE}/api/upload`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        error = `Upload failed: ${response.status}`;
        return;
      }

      // Read blob
      const blob = await response.blob();

      // Parse server filename from Content-Disposition (RFC 5987)
      const cd = response.headers.get("Content-Disposition") ?? "";
      const m = /filename\*?=(?:UTF-8'')?["']?([^"';]+)["']?/i.exec(cd);
      if (m && m[1]) {
        try {
          suggestedFilename = decodeURIComponent(m[1]);
        } catch {
          suggestedFilename = m[1];
        }
      } else {
        // Fallback: original base + blob type
        const base = (selectedFile.name ?? "cutout").replace(/\.[^/.]+$/, "");
        const ext = blob.type?.split("/")[1] ?? "png";
        suggestedFilename = `${base}-cutout.${ext}`;
      }

      // Swap out the object URL
      if (displayImageUrl) URL.revokeObjectURL(displayImageUrl);
      displayImageUrl = URL.createObjectURL(blob);
    } catch (err: any) {
      error = "Request failed: " + err.message;
    } finally {
      isLoading = false;
      processedCutout = true;
    }
  }

  const debouncedProcess = debounce(() => {
    if (selectedFile) uploadData();
  }, debounceTiming);

  $effect(() => {
    if (selectedFile) {
      fileChanged = true;
    }
  });

  $effect(() => {
    if (selectedFile && outlineThickness && detailValue && outlineColor) {
      if (fileChanged) {
        if (displayImageUrl) URL.revokeObjectURL(displayImageUrl);
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
    if (displayImageUrl) URL.revokeObjectURL(displayImageUrl);
  });
</script>

<div class="flex flex-col h-screen p-4 gap-4">
  <Navbar />
  <div class="flex flex-col items-center flex-1 gap-6">
    <h1 class="text-3xl font-semibold">Create a Cutout</h1>
    <div class="flex flex-col md:flex-row flex-1 max-w-4xl gap-8 p-2 items-center">
      <SelectImage bind:selectedFile={selectedFile} {displayImageUrl} {isLoading} />
      <CutoutOptions
        bind:outlineThickness
        bind:detailValue
        bind:outlineColor
        {processedCutout}
        imageUrl={displayImageUrl}
        suggestedFilename={suggestedFilename}
      />
    </div>
  </div>
</div>