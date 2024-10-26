# SSUphysics experiment supporting tools
숭실대학교 물리학과 물리계측실험 수업에서 유용하게 사용할 수 있는 python 페키지입니다.

> 향후 다른 실험 수업에서도 사용할 수 있도록 확장할 예정입니다.

## How to install
```zsh
pip install SSUphysicsTools
```

## How to use
### getting data
getting_data.py 파일을 이용하여 실험 데이터를 가져올 수 있습니다.
- pairwise_to_2d_list
- get_sorted_folders_dir_by_number
- get_channel_csv_files
- read_csv_Tektronix
- get_all_csv_paths
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