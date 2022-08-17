clear;clc;
data_path = 'F:\Ye\eeg_script\outData\fixation\converMark';
save_path = 'F:\Ye\eeg_script\outData\fixation\sep';
erp_path = 'F:\Ye\eeg_script\outData\fixation\erp';
erp_txt = 'F:\Ye\eeg_script\outData\fixation\erp_txt';
% file = 'sub88.set';
file_lists = dir(fullfile(data_path, '*.set'));
for i=1:length(file_lists)
    file = file_lists(i).name; 
    file_split = split(file, ".");
    sub = cell2mat(file_split(1));

    [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
    EEG = pop_loadset('filename', file, 'filepath', data_path);
    [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1); 
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_creabasiceventlist( EEG , 'AlphanumericCleaning', 'on', 'BoundaryNumeric', { -99 }, 'BoundaryString', { 'boundary' }, 'Eventlist', [erp_txt '\' sub '_eventList.txt']);
    EEG = eeg_checkset( EEG );
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG  = pop_binlister( EEG , 'BDF', [erp_txt '\mark.txt'], 'ExportEL', [erp_txt '\' sub '_outMark.txt'], 'IndexEL',  1, 'SendEL2', 'EEG&Text', 'Voutput', 'EEG' ); % 
    EEG = eeg_checkset( EEG );
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG = pop_epochbin( EEG , [-200.0  800.0],  'pre');
    EEG = eeg_checkset( EEG );
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    EEG  = pop_artextval( EEG , 'Channel',  1:61, 'Flag',  1, 'LowPass',  -1, 'Threshold', [ -100 100], 'Twindow', [ -200 0] );
    % EEG  = pop_artmwppth( EEG , 'Channel',  1:61, 'Flag',  1, 'LowPass',  -1, 'Threshold',  80, 'Twindow', [ -200 0], 'Windowsize',  200, 'Windowstep',  100 );
    EEG = eeg_checkset( EEG );
    [ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);
    ERP = pop_averager( ALLEEG , 'Criterion', 'good', 'DQ_custom_wins', 0, 'DQ_flag', 1, 'DQ_preavg_txt', 0, 'DSindex', 1, 'ExcludeBoundary',...
     'on', 'SEM', 'on' );
    ERP = pop_savemyerp(ERP, 'erpname', sub, 'filename', [sub 'erp.erp'], 'filepath', erp_path, 'Warning', 'on');
    % ERP ÂË²¨ 30Hz
    ERP = pop_filterp( ERP,  1:61 , 'Cutoff',  30, 'Design', 'butter', 'Filter', 'lowpass', 'Order',  2 );
    ERP = pop_averager( ALLEEG , 'Criterion', 'good', 'DQ_custom_wins', 0, 'DQ_flag', 1, 'DQ_preavg_txt', 0, 'DSindex', 1, 'ExcludeBoundary',...
     'on', 'SEM', 'on' );
    ERP = pop_savemyerp(ERP, 'erpname', sub, 'filename', [sub 'erp2.erp'], 'filepath', erp_path, 'Warning', 'on');
end