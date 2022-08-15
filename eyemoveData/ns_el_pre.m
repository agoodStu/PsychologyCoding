clear;clc;
%%
dataPath='F:\Ye\eeg_script\data\fixation';
Subjects = {'sub28', 'sub29', 'sub30','sub31', 'sub32', 'sub33', 'sub34', 'sub35'};
% Subjects = {'sub41'};
filePath={'eye','eeg'};
savePath = 'F:\Ye\eeg_script\outData\fixation\preSep';
% saveName = ['sub', num2str(i), '.set'];



%% 循环
for i = 1: length(Subjects)
    sub = Subjects{i};
    disp([sub,' preprocessing......'])   
    %% eeg和eye文件夹
        
    eye_path=cell2mat(fullfile(dataPath,string(sub),filePath{1}));
    eeg_path=cell2mat(fullfile(dataPath,string(sub),filePath{2}));


    %% 导入原始脑电数据
    eeg_data = dir(fullfile(eeg_path, '*.cdt'));
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = loadcurry(fullfile(eeg_path, eeg_data.name), 'KeepTriggerChannel', 'True', 'CurryLocations', 'False');
    EEG = eeg_checkset( EEG );
    
    %% 将眼动数据添加到脑电中
    eye_data = dir(fullfile(eye_path,'*.asc'));  % 眼动原始文件
    ET = parseeyelink(fullfile(eye_path, eye_data.name), fullfile(eye_path, 'eye.mat'), 'MYKEYWORD');  %%转为眼动文件数据格式
    EEG = pop_importeyetracker(EEG,fullfile(eye_path, 'eye.mat'),[200 100] ,[1:7] ,{'TIME','L-GAZE-X','L-GAZE-Y','L-AREA','R-GAZE-X','R-GAZE-Y','R-AREA'},0,1,0,1,4);  %添加哪些数据
    EEG = eeg_checkset( EEG );

    %% 根据眼动位置拒绝眼动数据；检测燕条和注视，并添加到eeg的事件中
    EEG = pop_rej_eyecontin(EEG,[69 70 72 73] ,[1 1 1 1] ,[1280 1024 1280 1024] ,100,2);
    EEG = pop_detecteyemovements(EEG,[69 70] ,[72 73] ,6,4,0.030215,1,0,50,1,1,1,1);
    EEG = eeg_checkset( EEG );

    %% 滤波和重参考
    EEG = applytochannels(EEG, [1:67] ,' pop_eegfiltnew(EEG, ''locutoff'',1,''plotfreqz'',1);');
    EEG = applytochannels(EEG, [1:67] ,' pop_eegfiltnew(EEG, ''hicutoff'',30,''plotfreqz'',1);');
    EEG = eeg_checkset( EEG );
    EEG = pop_reref( EEG, [33 43] );
    EEG = eeg_checkset( EEG );
    
    %% 剔除无用电极
    EEG = pop_select( EEG, 'nochannel',{'HEO','VEO','TRIGGER','TIME'});
    EEG = eeg_checkset( EEG );
    


    %% ICA和去眼动伪迹
    EEG = pop_runica(EEG, 'icatype', 'runica', 'extended',1,'interrupt','on','pca',68);
    EEG = eeg_checkset( EEG );
    [EEG vartable] = pop_eyetrackerica(EEG,'saccade','fixation',[10 0] ,1.1,3,1,1);
    EEG = eeg_checkset( EEG );

    
    EEG = pop_select( EEG, 'nochannel',{'L-GAZE-X','L-GAZE-Y','L-AREA','R-GAZE-X','R-GAZE-Y','R-AREA'});

    
    %% 保存数据
    saveName = [sub, '.set'];
    EEG = pop_saveset(EEG, 'filename',saveName,'filepath',savePath);

end