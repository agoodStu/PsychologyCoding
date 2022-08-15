clear;clc;
%%
dataPath='F:\Ye\eeg_script\data\fixation';
% Subjects = {'sub16','sub17', 'sub18', 'sub19', 'sub20', 'sub21', 'sub22','sub23', 'sub24', 'sub25', 'sub26', 'sub27', 'sub28', 'sub229', 'sub30','sub31', 'sub32', 'sub33', 'sub34', 'sub35'};
Subjects = {'sub88'};
filePath={'eye','eeg'};
savePath = 'F:\Ye\eeg_script\outData\fixation\preSep';
% saveName = ['sub', num2str(i), '.set'];



%% ѭ��
for i = 1: length(Subjects)
    sub = Subjects{i};
    disp([sub,' preprocessing......'])   
    %% eeg��eye�ļ���
        
    eye_path=cell2mat(fullfile(dataPath,string(Subjects{1}),filePath{1}));
    eeg_path=cell2mat(fullfile(dataPath,string(Subjects{1}),filePath{2}));


    %% ����ԭʼ�Ե�����
    eeg_data = dir(fullfile(eeg_path, '*.vhdr'));
    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
%     EEG = loadcurry(fullfile(eeg_path, eeg_data.name), 'KeepTriggerChannel', 'True', 'CurryLocations', 'False');
    EEG = pop_loadbv(eeg_path, eeg_data.name, [1 523800], [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64]);
    EEG = eeg_checkset( EEG );
    
    %% ���۶�������ӵ��Ե���
    eye_data = dir(fullfile(eye_path,'*.asc'));  % �۶�ԭʼ�ļ�
    ET = parseeyelink(fullfile(eye_path, eye_data.name), fullfile(eye_path, 'eye.mat'), 'MYKEYWORD');  %%תΪ�۶��ļ����ݸ�ʽ
    EEG = pop_importeyetracker(EEG,fullfile(eye_path, 'eye.mat'),[200 100] ,[1:11] ,{'TIME','L-GAZE-X','L-GAZE-Y','L-AREA','R-GAZE-X','R-GAZE-Y','R-AREA','INPUT','targetpos-x','targetpos-y','targetdistance'},0,1,0,1,4);  %�����Щ����
    EEG = eeg_checkset( EEG );

    %% �����۶�λ�þܾ��۶����ݣ����������ע�ӣ�����ӵ�eeg���¼���
    EEG = pop_rej_eyecontin(EEG,[66 67 69 70] ,[1 1 1 1] ,[1280 1024 1280 1024] ,100,2);
    EEG = pop_detecteyemovements(EEG,[66 67] ,[69 70] ,6,4,0.030215,1,0,50,1,1,1,1);
    EEG = eeg_checkset( EEG );

    %% �˲����زο�
    EEG = applytochannels(EEG, [1:64] ,' pop_eegfiltnew(EEG, ''locutoff'',1,''plotfreqz'',1);');
    EEG = applytochannels(EEG, [1:64] ,' pop_eegfiltnew(EEG, ''hicutoff'',30,''plotfreqz'',1);');
    EEG = eeg_checkset( EEG );
    EEG = pop_reref( EEG, [31 32] );
    EEG = eeg_checkset( EEG );
    
    %% �޳����õ缫
    EEG = pop_select( EEG, 'nochannel',{'VEOG','TIME','INPUT','targetpos-x','targetpos-y','targetdistance'});
    EEG = eeg_checkset( EEG );
    


    %% ICA��ȥ�۶�α��
    EEG = pop_runica(EEG, 'icatype', 'runica', 'extended',1,'interrupt','on','pca',62);
    EEG = eeg_checkset( EEG );
    [EEG vartable] = pop_eyetrackerica(EEG,'saccade','fixation',[10 0] ,1.1,3,1,1);
    EEG = eeg_checkset( EEG );

    
    EEG = pop_select( EEG, 'nochannel',{'L-GAZE-X','L-GAZE-Y','L-AREA','R-GAZE-X','R-GAZE-Y','R-AREA'});

    
    %% ��������
    saveName = [sub, '.set'];
    EEG = pop_saveset(EEG, 'filename',saveName,'filepath',savePath);

end


% %% �ֶ�
% sepSavePath = 'F:\Ye\eeg_script\outData\fixation\sep';
% for j = 1: length(Subjects)
%     sub = Subjects{j};
%     sep_eeg_name = ['sub41','_r.set'];
%     % �ֶο�ʼ
%     EEG = pop_loadset('filename', sep_eeg_name, 'filepath', savePath);
%     EEG = pop_epoch( EEG, { '111' '112' '121' '122' '233'}, [5.5  0], 'newname', 'eyeEeg-dect-filter-reRef pruned with ICA epochs', 'epochinfo', 'yes');
%     EEG = pop_epoch( EEG, {  '150'  }, [-0.2         5.6], 'newname', 'Neuroscan Curry file pruned with ICA epochs', 'epochinfo', 'yes');
%         EEG = applytochannels(EEG, [1:62] ,' pop_rmbase( EEG, [-200 0] ,[]);');
%     EEG = eeg_checkset( EEG );
%     EEG = pop_rmbase( EEG, [-200 0] ,[]);
%     EEG = eeg_checkset( EEG );
%     
%     % �洢����
%     sep_save_name = [sub, '_sep.set'];
%     EEG = pop_saveset(EEG, 'filename',sep_save_name,'filepath',sepSavePath);
% end