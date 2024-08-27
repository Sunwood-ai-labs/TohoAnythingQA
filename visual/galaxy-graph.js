import * as THREE from 'three';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';

function initGraph() {
    const N = 300;
    const BLOOM_INTENSITY = 3.5;
    const MAX_EMISSIVE_INTENSITY = 25;

    // 提供されたカラーパレットを定義
    const starColors = [
        0x0E1826,
        0xF2AB6D,
        0xD9501E,
        0xD98C71,
        0x592222
    ];

    const gData = {
        nodes: [...Array(N).keys()].map(i => ({ 
            id: i,
            color: starColors[Math.floor(Math.random() * starColors.length)],
            emissiveIntensity: Math.random() * MAX_EMISSIVE_INTENSITY
        })),
        links: [...Array(N).keys()]
            .filter(id => id)
            .map(id => ({
                source: id,
                target: Math.round(Math.random() * (id - 1))
            }))
    };

    const Graph = ForceGraph3D({
        rendererConfig: {
            outputEncoding: THREE.sRGBEncoding,
            toneMapping: THREE.ACESFilmicToneMapping,
            toneMappingExposure: 1.5,
        }
    })(document.getElementById('graph'))
        .graphData(gData)
        .backgroundColor('#000000')  // 背景色を最も暗い色に設定
        .nodeThreeObject(node => {
            const material = new THREE.MeshStandardMaterial({
                color: node.color,
                emissive: node.color,
                emissiveIntensity: node.emissiveIntensity
            });
            return new THREE.Mesh(new THREE.SphereGeometry(4), material);
        })
        .linkWidth(1)
        .linkOpacity(0.5)
        .linkColor(() => '#ffffff')
        .d3AlphaDecay(0.01)
        .d3VelocityDecay(0.1);

    // Bloom効果の追加
    const bloomPass = new UnrealBloomPass(
        new THREE.Vector2(window.innerWidth, window.innerHeight),
        BLOOM_INTENSITY,
        0.4,
        0.85
    );
    Graph.postProcessingComposer().addPass(bloomPass);

    // OrbitControlsの設定を調整
    const controls = Graph.controls();

    // 初期カメラ位置の設定
    Graph.cameraPosition({ x: 400, y: 400, z: 400 });

    // グラフが安定したら、全体が見えるようにズーム
    Graph.onEngineStop(() => {
        Graph.zoomToFit(400, 100);
    });

    // アニメーションループの設定
    function animate() {
        if (controls) controls.update();
        requestAnimationFrame(animate);
    }
    animate();

    // ウィンドウリサイズ時の処理
    window.addEventListener('resize', () => {
        Graph.width(window.innerWidth);
        Graph.height(window.innerHeight);
    });
}

// DOMContentLoadedイベントでinitGraph関数を呼び出す
document.addEventListener('DOMContentLoaded', initGraph);
