import toml from "@fbraem/rollup-plugin-toml";
import dts from 'vite-plugin-dts';
import {defineConfig} from "vite";
import {resolve} from "path";

export default defineConfig({
    plugins: [
        toml(),
        dts()
    ],
    build: {
        lib: {
            entry: resolve(__dirname, "src/config.toml"),
            name: "@kwai/config",
            fileName: "kwai-config"
        },
        rollupOptions: {
            output: {
                exports: "named"
            }
        }
    }
})
