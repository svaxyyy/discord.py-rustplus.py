@echo off
cls
npx @liamcottle/rustplus.js fcm-register
cls
npx @liamcottle/rustplus.js fcm-listen
npx @liamcottle/rustplus.js --config-file=%cd%/output.json