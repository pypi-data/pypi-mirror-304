# SSUphysics experiment supporting tools
숭실대학교 물리학과 물리계측실험 수업에서 유용하게 사용할 수 있는 python 페키지입니다.

> 향후 다른 실험 수업에서도 사용할 수 있도록 확장할 예정입니다.

## How to install
```zsh
pip install SSUphysicsTools
```

## Example
다음의 repository를 참고하여 사용할 수 있습니다.
[SSUphysicsTools-example](https://github.com/kty1004/SSUphysicsTools_examples)

## How to use
### Setting up
실험 데이터는 data 폴더에 저장되어 있어야 합니다. 이 때 data 폴더는 다음과 같은 구조를 가지고 있어야 합니다.
```
data
├── experiment 1
│   ├── 1.csv
│   ├── 2.csv
├── experiment 2
│   ├── 1.csv
│   ├── 2.csv
└── ...
```
만약 data 폴더가 준비되지 않았더면, 자동으로 data 폴더를 생성하고 `DataDirectoryEmptyError`를 발생시켜 data 폴더에 실험 데이터를 넣도록 알려줍니다.

### getting data
get_all_csv_paths method를 이용하여 실험 데이터를 가져올 수 있습니다.

### processing data
- Regression
    - cosine_regression
- Delate_offset
### analyzing data
- Phase_shift
    - find_min_x_vector
    - find_ym_y0
- get_error_rate
### plot
- Plots
    - rough data plot
    - bode plot
- plot_table