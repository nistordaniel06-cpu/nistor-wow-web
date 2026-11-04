# NISTOR WoW

## V1 — browser demo

`index.html` is a standalone, mobile-friendly fantasy game prototype. Open locally or publish with GitHub Pages. Features: touch joystick, keyboard movement, attack/spell buttons, enemies and score. **It is not connected to AzerothCore and does not contain Blizzard game assets.**

## Publishing

GitHub → Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save. Expected URL after publishing: `https://nistordaniel06-cpu.github.io/nistor-wow-web/`.

## Future phases

1. Prototype player UI, character selection and authentication against a purpose-built backend (never put database credentials in browser code).
2. Evaluate browser client engines and compatibility with AzerothCore 3.3.5a build 12340; implement protocol and authentication with appropriate security and legal review.
3. Render original/licensed 3D world assets, NPCs, combat and touch controls.
4. Test gameplay with the locally hosted AzerothCore server; a public hosted webpage cannot connect to the phone's `127.0.0.1` and requires a secure, reachable gateway.

Do not expose MariaDB, authserver or worldserver directly to the public internet.