# 流体シミュレーションの実装
流体シミュレーションの手法のうち、粒子法のSPH法と位置ベース法のPBF法を実装した。
### 実行環境
以下の環境で実行を行いました。open3Dはシミュレーションの可視化用に用いたライブラリ、点群やメッシュなどの可視化を行うことができる。
- wsl2(Ubuntu22.04)
- Python3 3.10.9
- numpy 1.24.3
- open3D 0.17.0

### SPH（Smoothed Particle Hydrodynamics）法
#### 実装の工夫について
- 近傍粒子を探索するに領域を分割し、近傍領域の粒子のみに限定することで計算量を減らした。実行時間は全粒子数が6920の時、探索時間が22.1257から0.92952へと大幅に短縮しており、計算量低減の効果は高いと思われる。

- スレッドを用い、並列性を高め実行時間を短縮させた。
#### 実行デモ
粒子サイズが0.01、影響半径h=0.015、流体の粒子数=864、壁の厚さ=0.04、実行時間（フレーム数）=300フレームで行った。
https://www.youtube.com/watch?v=_55yv8_HHiM
### PBF（Positon Based Fluids）法
#### 実装の工夫
- 近傍粒子を探索するに領域を分割し、近傍領域の粒子のみに限定することで計算量を減らした。実行時間は全粒子数が＿の時変化した。

- スレッドを用い、並列性を高め実行時間を短縮させた。
#### 実行デモ
粒子サイズが0.01、影響半径h=0.015、流体の粒子数=936、壁の厚さ=0.04、実行時間（フレーム数）=300フレームで行った。
https://www.youtube.com/watch?v=pxA4nZMnYKU
### 実行・可視化について
実行は各ディレクトリで以下のコマンドで行える。
```
python3 main.py (流体の粒子数) (イテレーション数)
```

可視化は各ディレクトリで以下のコマンドで行える。
```
python3 visualize.py (流体の粒子数) (イテレーション数)
```
### 参考資料

- PBF実装に関して
Macklin, Miles, and Matthias Müller. "Position based fluids." ACM Transactions on Graphics (TOG) 32.4 (2013): 1-12.# project
