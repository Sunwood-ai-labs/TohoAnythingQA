import * as THREE from 'three';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';

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

function initGraph() {
    fetch('../neo4j_import/neo4j_blocks.json')
        .then(res => res.json())
        .then(data => {
            const nodes = data.nodes.map(node => ({
                id: node.id,
                color: starColors[Math.floor(Math.random() * starColors.length)],
                emissiveIntensity: Math.random() * MAX_EMISSIVE_INTENSITY + 5,
                description: node.description || `Node ${node.id}`,
                // 他のノードプロパティをここに追加
            }));

            const links = data.links.map(link => ({
                source: link.source,
                target: link.target,
                // 他のリンクプロパティをここに追加
            }));

            const gData = { nodes, links };

            const Graph = ForceGraph3D({
                rendererConfig: {
                    outputEncoding: THREE.sRGBEncoding,
                    toneMapping: THREE.ACESFilmicToneMapping,
                    toneMappingExposure: 1.5,
                }
            })(document.getElementById('graph'))
                .graphData(gData)
                .backgroundColor('#000000')
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
                .linkCurvature("curvature")
                .linkColor(() => '#ffffff')
                .d3AlphaDecay(0.01)
                .d3VelocityDecay(0.1)
                .nodeLabel(node => node.description)
                .onNodeHover(node => {
                    document.getElementById('graph').style.cursor = node ? 'pointer' : 'default';
                })
                .linkDirectionalParticles(4)
                .onNodeClick((node, event) => {
                    // Aim at node from outside it
                    const distance = 10;
                    const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);

                    Graph.cameraPosition(
                        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
                        node, // lookAt ({ x, y, z })
                        3000  // ms transition duration
                    );
                });

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
            Graph.cameraPosition({ x: 40, y: 40, z: 40 });

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
        })
        .catch(error => console.error('Error loading the JSON file:', error));
}

// DOMContentLoadedイベントでinitGraph関数を呼び出す
document.addEventListener('DOMContentLoaded', initGraph);
