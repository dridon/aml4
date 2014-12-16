clear all; clc
tic
file_read = 'V:\Laboratoires\Rabasa-Lhoret\Projets PROMD\Études en cours\Études académiques\CLASS03\Data and Statistics\XT_Files and Code\CLASS03_data.xlsx';
all_pts=[1,2,3,4,6,7,8,9,10,12,13,14,16,17,18,19,20,21,23,24,26,28,29,30,32,33,34,35,36];
n = length(all_pts);  

[~, ~, date_OL]=xlsread(file_read,'5.Reference Glucose (Plasma)','C5:AE6');      %OPEN LOOP  % 3 CELLS WITH THE DATES FOR CSII, SINGLE AND DUAL HORMONE TRIALS 
[~, ~, date_S]=xlsread(file_read,'5.Reference Glucose (Plasma)','C305:AE306');   %SINGLE
[~, ~, date_D]=xlsread(file_read,'5.Reference Glucose (Plasma)','C605:AE606');   %DUAL
fprintf('Dates OK\n')
CLASS03=zeros(3,n);                                                             % INFO ABOUT PATIENTS IN CLASS03 (WEIGHT, TOTAL DAILY DOSE, BASAL)

weight=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C6:CJ6'); 
weight(isnan(weight))=[]; 
CLASS03(1,1:n)=weight; %WEIGHT

TDD=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C8:CJ8');    
TDD(isnan(TDD))=[];       
CLASS03(2,1:n)=TDD;    %TOTAL DAILY DOSE

basal=xlsread(file_read,'1.Basal Rates','C54:AE54');                   
basal(isnan(basal))=[];   
CLASS03(3,1:n)=basal;  %BASAL LEVEL

ICR=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C2:CJ5');              %INSULIN TO CARBOHYDRATES RATIO
[~,ICR_time,~]=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','A2:A5');
basal_rates=xlsread(file_read,'1.Basal Rates','C5:AE52');                        %basal rates

Meal_OL=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C13:CJ26');        %OPEN LOOP % MEAL, INSULIN AND GLUCAGON BOLUS: 
Meal_S=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C29:CJ39');         %SINGLE
Meal_D=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C42:CJ59');         %DUAL
fprintf('Meals OK\n')
InsBol_OL=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C63:CJ68'); 
InsBol_S=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C71:CJ76'); 
InsBol_D=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C79:CJ83'); 
fprintf('Insulin OK\n')
GluBol_D=xlsread(file_read,'2.Ratio, Weight, Meal and Ins B','C87:CJ230');      %DUAL (GLUCAGON BOLUS)

ItimeOL=xlsread(file_read,'3.Insulin infusion','A5:A293'); time5 = datestr(ItimeOL,'HH:MM');  %time every 5 mins
ItimeS=xlsread(file_read,'3.Insulin infusion','A305:A449'); time10 = datestr(ItimeS,'HH:MM');   %time every 10 mins

InsInfOL=xlsread(file_read,'3.Insulin infusion','C5:AE293');                     %OPEN LOOP  % VARIABLES FOR THE INSULIN INFUSION DATA...                                                                                                                                                                                       
loc_dataIOL = ~isnan(InsInfOL);   
InsInfS=xlsread(file_read,'3.Insulin infusion','C305:AE449');                    %SINGLE 
loc_dataIS = ~isnan(InsInfS);                       
InsInfD=xlsread(file_read,'3.Insulin infusion','C455:AE599');                    %DUAL 
loc_dataID = ~isnan(InsInfD); 

GMOL=xlsread(file_read,'4.Glucose conc(sensor)','C10:AE298');                    %OPEN LOOP  % VARIABLES FOR THE GLUCOSE SENSOR                                                                                                                                                                                         
loc_dataGMOL = ~isnan(GMOL);   
GMS=xlsread(file_read,'4.Glucose conc(sensor)','C313:AE601');                    %SINGLE 
loc_dataGMS = ~isnan(GMS);   
GMD=xlsread(file_read,'4.Glucose conc(sensor)','C617:AE905');                    %DUAL 
loc_dataGMD = ~isnan(GMD);
fprintf('Sensor OK\n')

BGOL=xlsread(file_read,'5.Reference Glucose (Plasma)','C8:AE296');               %OPEN LOOP % VARIABLES FOR THE REFERENCE GLUCOSE (PLASMA)
loc_dataBGOL = ~isnan(BGOL);   
BGS=xlsread(file_read,'5.Reference Glucose (Plasma)','C308:AE596');              %SINGLE 
loc_dataBGS = ~isnan(BGS);   
BGD=xlsread(file_read,'5.Reference Glucose (Plasma)','C608:AE896');              %DUAL 
loc_dataBGD = ~isnan(BGD);
fprintf('YSI OK\n')

for i=1:n                                                                  %redefine the insulin variables so that they contain only non empty...
        InsInf_OL{i}= InsInfOL(loc_dataIOL(:,i),i);                             %values and store only the time that contains a certain plasma glucose value
        xtimestrI_OL{i} = time5(loc_dataIOL(:,i),:);                      %OPEN LOOP
        InsInf_S{i}= InsInfS(loc_dataIS(:,i),i);        
        xtimestrI_S{i} = time10(loc_dataIS(:,i),:);                         %SINGLE
        InsInf_D{i}= InsInfD(loc_dataID(:,i),i);        
        xtimestrI_D{i} = time10(loc_dataID(:,i),:);                         %DUAL %redefine the glucose sensor variables so that they contain only non empty
        GM_OL{i}= GMOL(loc_dataGMOL(:,i),i);                                        %values and store only the time that contains a certain plasma glucose value
        xtimestrGM_OL{i} = time5(loc_dataGMOL(:,i),:);                   %OPEN LOOP
        GM_S{i}= GMS(loc_dataGMS(:,i),i);        
        xtimestrGM_S{i} = time5(loc_dataGMS(:,i),:);                      %SINGLE
        GM_D{i}= GMD(loc_dataGMD(:,i),i);        
        xtimestrGM_D{i} = time5(loc_dataGMD(:,i),:);                      %DUAL %redefine the reference glucose variables so that they contain only non empty
        BG_OL{i}= BGOL(loc_dataBGOL(:,i),i);                                          %values and store only the time that contains a certain plasma glucose value
        xtimestrBG_OL{i} = time5(loc_dataBGOL(:,i),:);                   %OPEN LOOP
        BG_S{i}= BGS(loc_dataBGS(:,i),i);        
        xtimestrBG_S{i} =  time5(loc_dataBGS(:,i),:);                      %SINGLE
        BG_D{i}= BGD(loc_dataBGD(:,i),i);        
        xtimestrBG_D{i} = time5(loc_dataBGD(:,i),:);                      %DUAL
end
 fprintf('Loop OK\n')

[~, ~, name_OL] = xlsread(file_read,'5.Reference Glucose (Plasma)','C4:AE4');    %XT FILES, OPEN LOOP (OL):1st, read the name of the study, e.g. CLASS03_01_01
for j=1:n
    fid=fopen([name_OL{j} '.txt'],'wt');                                        %make the text file
    fprintf(fid,['ID: ' name_OL{j} ' \nWeight: \t   %0.0f' ' kg\n'],weight(j)); %ID, Weight
    fprintf(fid,['Today daily dose:  %0.2f U/day\n'],TDD(j));                   %TDD
    col_loc = 3*(j-1)+1;   %ICR  %
    l=1;
    fprintf(fid,['Ins to Carb Ratio: \n']);
    while l <= size(ICR,1) && ~isnan(ICR(l,col_loc))
        fprintf(fid,['\t' ICR_time{l} ': %0.2f U/10g\n'],ICR(l,col_loc));
        l=l+1;
    end    
    fprintf(fid,['Basal: \t\t   %0.1f U/day\n'],basal(j));   
    fprintf(fid,'Basal rate in 30min steps (U/h):\n\t');
    for i=1:(length(basal_rates)-1)
        fprintf(fid,'%0.2f ',basal_rates(i));    
        if mod(i,12)==0
        fprintf(fid, '\n\t');
        end
    end
    fprintf(fid, '\n\nEnteral_bolus (meal) ******************************************** \n');
    fprintf(fid,'Time \t\t\t CHO\n(dd/mm/yyyy hh:mm)\t (g)\n'); 
    col_loc = 3*(j-1) + 1;
    l = 1; 
    while l <= size(Meal_OL,1) && ~isnan(Meal_OL(l,col_loc))
        date_aux = datestr(Meal_OL(l,col_loc),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23                          %put the first date
            fprintf(fid,[date_OL{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],Meal_OL(l,col_loc+1));
        else                                                                                        %put the second date
            fprintf(fid,[date_OL{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],Meal_OL(l,col_loc+1));
        end
        l = l + 1;
    end
    col_loc=3*(j-1)+1;
    l=1;
   fprintf(fid,'\nInsulin_bolus *************************************************** \n');
   fprintf(fid,'Time \t\t\t Bolus \t Duration \t Insulin \n(dd/mm/yyyy hh:mm)\t (U) \t (min) \t\t (S|R|N) \n');
   while l <= size(InsBol_OL,1) && ~isnan(InsBol_OL(l,col_loc)) && ~(InsBol_OL(l,col_loc)==0.00)
        date_aux = datestr(InsBol_OL(l,col_loc),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23                          %put the first date
            fprintf(fid,[date_OL{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],InsBol_OL(l,col_loc+1));
        else                                                                                        %put the second date
            fprintf(fid,[date_OL{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],InsBol_OL(l,col_loc+1));
        end
        l = l + 1;
  end
 fprintf(fid,'\nGlucagon_bolus *************************************************** \n');
 fprintf(fid,'Time \t\t\t Bolus \n(dd/mm/yyyy hh:mm)\t (U) \n');                                    %Glucagon Bolus for Dual Closed Loop Only
 fprintf(fid,'\nInsulin_infusion ******************************************** \n');                 %insulin infusion header 
 fprintf(fid,'Time \t\t\t Rate \n(dd/mm/yyyy hh:mm)\t (U/h) \n');
     for i=1:(length(InsInf_OL{j})-1)
        if str2num(xtimestrI_OL{j}(i,1:2)) >= 8 && str2num(xtimestrI_OL{j}(i,1:2)) <= 23            %put the first date
            fprintf(fid,[date_OL{1,j} ' ' xtimestrI_OL{j}(i,:) '\t %0.2f' '\n'],InsInf_OL{j}(i));
        else                                                                                        %put the second date
            fprintf(fid,[date_OL{2,j} ' ' xtimestrI_OL{j}(i,:) '\t %0.2f' '\n'],InsInf_OL{j}(i));
        end
     end
     if ~isempty(InsInf_OL{j})
         fprintf(fid,[date_OL{2,j} ' ' xtimestrI_OL{j}(end,:) '\t %0.2f' '\n'],InsInf_OL{j}(end));  %correction for last date
     end
  fprintf(fid,'\nGlucose_concentration ******************************************** \n');
  fprintf(fid,'Time \t\t\t Conc \n(dd/mm/yyyy hh:mm)\t (mmol/L) \n');
     for i=1:(length(GM_OL{j})-1)
        if str2num(xtimestrGM_OL{j}(i,1:2)) >= 8 && str2num(xtimestrGM_OL{j}(i,1:2)) <= 23          %put the first date
            fprintf(fid,[date_OL{1,j} ' ' xtimestrGM_OL{j}(i,:) '\t %0.2f' '\n'],GM_OL{j}(i));
        else                                                                                        %put the second date
            fprintf(fid,[date_OL{2,j} ' ' xtimestrGM_OL{j}(i,:) '\t %0.2f' '\n'],GM_OL{j}(i));
        end
     end
     if ~isempty(GM_OL{j})
         fprintf(fid,[date_OL{2,j} ' ' xtimestrGM_OL{j}(end,:) '\t %0.2f' '\n'],GM_OL{j}(end));     %correction for last date
     end
  fprintf(fid,'\nReference_glucose_concentration ******************************************** \n');
  fprintf(fid,'Time \t\t\t Conc \n(dd/mm/yyyy hh:mm)\t (mmol/L) \n');
     for i=1:(length(BG_OL{j})-1)
        if str2num(xtimestrBG_OL{j}(i,1:2)) >= 8 && str2num(xtimestrBG_OL{j}(i,1:2)) <= 23          %put the first date
            fprintf(fid,[date_OL{1,j} ' ' xtimestrBG_OL{j}(i,:) '\t %0.2f' '\n'],BG_OL{j}(i));
        else                                                                                        %put the second date
            fprintf(fid,[date_OL{2,j} ' ' xtimestrBG_OL{j}(i,:) '\t %0.2f' '\n'],BG_OL{j}(i));
        end
     end
     if ~isempty(BG_OL{j})
         fprintf(fid,[date_OL{2,j} ' ' xtimestrBG_OL{j}(end,:) '\t %0.2f' '\n'],BG_OL{j}(end));     %correction for last date
     end
  fprintf(fid,'\nPlasma_insulin_concentration ******************************************** \nTime \t\t\tconc \n(dd/mm/yyyy hh:mm)');
  fprintf(fid,'\t(pmol/L) \n\nStart ******************************************** \nTime \n(dd/mm/yyyy hh:mm) \n');
fprintf(fid,[date_OL{1,j} ' 08:00 \nEND']);
end
fprintf('Finished .txt files(csii) \n')
[~, ~, name_S] = xlsread(file_read,'5.Reference Glucose (Plasma)','C304:AE304'); %XT FILES, SINGLE LOOP(S):1st, read the name of the study, e.g. CLASS03_01_01
for j=1:n
    fid=fopen([name_S{j} '.txt'],'wt');                                         %make the text file
    fprintf(fid,['ID: ' name_S{j} ' \nWeight: \t   %0.0f' ' kg\n'],weight(j));  %ID, Weight
    fprintf(fid,['Today daily dose:  %0.2f U/day\n'],TDD(j));                   %TDD
    col_loc = 3*(j-1)+1;                                                        %ICR  
    l=1;
    fprintf(fid,['Ins to Carb Ratio: \n']);
    while l <= size(ICR,1) && ~isnan(ICR(l,col_loc))
        fprintf(fid,['\t' ICR_time{l} ': %0.2f U/10g\n'],ICR(l,col_loc));
        l=l+1;
    end    
    fprintf(fid,['Basal: \t\t   %0.1f U/day\n'],basal(j));   
    fprintf(fid,'Basal rate in 30min steps (U/h):\n\t');
    for i=1:(length(basal_rates)-1)
    fprintf(fid,'%0.2f ',basal_rates(i));    
        if mod(i,12)==0
        fprintf(fid, '\n\t');
        end
    end
    fprintf(fid, '\n\nEnteral_bolus (meal) ******************************************** \n');
    fprintf(fid,'Time \t\t\t CHO\n(dd/mm/yyyy hh:mm)\t (g)\n'); 
    col_loc = 3*(j-1) + 1;
    l = 1; 
    while l <= size(Meal_S,1) && ~isnan(Meal_S(l,col_loc))
        date_aux = datestr(Meal_S(l,col_loc),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23        %put the first date
            fprintf(fid,[date_S{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],Meal_S(l,col_loc+1));
        else                                                                      %put the second date
            fprintf(fid,[date_S{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],Meal_S(l,col_loc+1));
        end
        l = l + 1;
    end
    col_loc=3*(j-1)+1;
    l=1;
    fprintf(fid,'\nInsulin_bolus *************************************************** \n');
    fprintf(fid,'Time \t\t\t Bolus \t Duration \t Insulin \n(dd/mm/yyyy hh:mm)\t (U) \t (min) \t\t (S|R|N) \n');
  while l <= size(InsBol_S,1) && ~isnan(InsBol_S(l,col_loc))&& ~(InsBol_S(l,col_loc)==0.00)
        date_aux = datestr(InsBol_S(l,col_loc),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23                          %put the first date
            fprintf(fid,[date_S{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],InsBol_S(l,col_loc+1));
        else                                                                                        %put the second date
            fprintf(fid,[date_S{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],InsBol_S(l,col_loc+1));
        end
        l = l + 1;
  end
  fprintf(fid,'\nGlucagon_bolus *************************************************** \n');
  fprintf(fid,'Time \t\t\t Bolus \n(dd/mm/yyyy hh:mm)\t (U) \n');                                   %Glucagon Bolus for Dual Closed Loop Only
  fprintf(fid,'\nInsulin_infusion ******************************************** \n');                %insulin infusion header 
  fprintf(fid,'Time \t\t\t Rate \n(dd/mm/yyyy hh:mm)\t (U/h) \n');
     for i=1:(length(InsInf_S{j})-1)
        if str2num(xtimestrI_S{j}(i,1:2)) >= 8 && str2num(xtimestrI_S{j}(i,1:2)) <= 23              %put the first date
            fprintf(fid,[date_S{1,j} ' ' xtimestrI_S{j}(i,:) '\t %0.2f' '\n'],InsInf_S{j}(i));
        else                                                                                        %put the second date
            fprintf(fid,[date_S{2,j} ' ' xtimestrI_S{j}(i,:) '\t %0.2f' '\n'],InsInf_S{j}(i));
        end
     end
     if ~isempty(InsInf_S{j})
         fprintf(fid,[date_S{2,j} ' ' xtimestrI_S{j}(end,:) '\t %0.2f' '\n'],InsInf_S{j}(end));     %correction for last date
     end
  fprintf(fid,'\nGlucose_concentration ******************************************** \n');
  fprintf(fid,'Time \t\t\t Conc \n(dd/mm/yyyy hh:mm)\t (mmol/L) \n');
     for i=1:(length(GM_S{j})-1)
        if str2num(xtimestrGM_S{j}(i,1:2)) >= 8 && str2num(xtimestrGM_S{j}(i,1:2)) <= 23            %put the first date
            fprintf(fid,[date_S{1,j} ' ' xtimestrGM_S{j}(i,:) '\t %0.2f' '\n'],GM_S{j}(i));
        else                                                                                        %put the second date
            fprintf(fid,[date_S{2,j} ' ' xtimestrGM_S{j}(i,:) '\t %0.2f' '\n'],GM_S{j}(i));
        end
     end
     if ~isempty(GM_S{j})
         fprintf(fid,[date_S{2,j} ' ' xtimestrGM_S{j}(end,:) '\t %0.2f' '\n'],GM_S{j}(end));        %correction for last date
     end
  fprintf(fid,'\nReference_glucose_concentration ******************************************** \n');
  fprintf(fid,'Time \t\t\t Conc \n(dd/mm/yyyy hh:mm)\t (mmol/L) \n');
     for i=1:(length(BG_S{j})-1)
        if str2num(xtimestrBG_S{j}(i,1:2)) >= 8 && str2num(xtimestrBG_S{j}(i,1:2)) <= 23            %put the first date
            fprintf(fid,[date_S{1,j} ' ' xtimestrBG_S{j}(i,:) '\t %0.2f' '\n'],BG_S{j}(i));
        else                                                                                        %put the second date
            fprintf(fid,[date_S{2,j} ' ' xtimestrBG_S{j}(i,:) '\t %0.2f' '\n'],BG_S{j}(i));
        end
     end
     if ~isempty(BG_S{j})
         fprintf(fid,[date_S{2,j} ' ' xtimestrBG_S{j}(end,:) '\t %0.2f' '\n'],BG_S{j}(end));        %correction for last date
     end
     fprintf(fid,'\nPlasma_insulin_concentration ******************************************** \nTime \t\t\tconc \n(dd/mm/yyyy hh:mm)');
fprintf(fid,'\t(pmol/L) \n\nStart ******************************************** \nTime \n(dd/mm/yyyy hh:mm) \n');
fprintf(fid,[date_S{1,j} ' 08:00 \nEND']);
end
fprintf('Finished .txt files(single) \n')

[~, ~, name_D] = xlsread(file_read,'5.Reference Glucose (Plasma)','C604:AE604');%XT FILES, DUAL LOOP (D):1st, read the name of the study, ex. CLASS03_01_01
for j=1:n
    fid=fopen([name_D{j} '.txt'],'wt');                                         %make the text file
    fprintf(fid,['ID: ' name_D{j} ' \nWeight: \t   %0.0f' ' kg\n'],weight(j));  % ID, Weight
    fprintf(fid,['Today daily dose:  %0.2f U/day\n'],TDD(j));                   %TDD
    col_loc = 3*(j-1)+1;                                                        %ICR  
    l=1;
    fprintf(fid,['Ins to Carb Ratio: \n']);
    while l <= size(ICR,1) && ~isnan(ICR(l,col_loc))
        fprintf(fid,['\t' ICR_time{l} ': %0.2f U/10g\n'],ICR(l,col_loc));
        l=l+1;
    end    
    fprintf(fid,['Basal: \t\t   %0.1f U/day\n'],basal(j));   
    fprintf(fid,'Basal rate in 30min steps (U/h):\n\t');
    for i=1:(length(basal_rates)-1)
    fprintf(fid,'%0.2f ',basal_rates(i));    
        if mod(i,12)==0
        fprintf(fid, '\n\t');
        end
    end
    fprintf(fid, '\n\nEnteral_bolus (meal) ******************************************** \n');
    fprintf(fid,'Time \t\t\t CHO\n(dd/mm/yyyy hh:mm)\t (g)\n'); 
    col_loc = 3*(j-1) + 1;
    l = 1; 
    while l <= size(Meal_D,1) && ~isnan(Meal_D(l,col_loc))
        date_aux = datestr(Meal_D(l,col_loc),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23        %put the first date
            fprintf(fid,[date_D{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],Meal_D(l,col_loc+1));
        else                                                                      %put the second date
            fprintf(fid,[date_D{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],Meal_D(l,col_loc+1));
        end
        l = l + 1;
    end
    col_loc=3*(j-1)+1;
    l=1;
    fprintf(fid,'\nInsulin_bolus *************************************************** \n');
    fprintf(fid,'Time \t\t\t Bolus \t Duration \t Insulin \n(dd/mm/yyyy hh:mm)\t (U) \t (min) \t\t (S|R|N) \n');
  while l <= size(InsBol_D,1) && ~isnan(InsBol_D(l,col_loc)) && ~(InsBol_D(l,col_loc)==0.00)
        date_aux = datestr(InsBol_D(l,col_loc),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23        %put the first date
            fprintf(fid,[date_D{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],InsBol_D(l,col_loc+1));
        else                                                                      %put the second date
            fprintf(fid,[date_D{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],InsBol_D(l,col_loc+1));
        end
        l = l + 1;
  end
  fprintf(fid,'\nGlucagon_bolus *************************************************** \n');
  fprintf(fid,'Time \t\t\t Bolus \n(dd/mm/yyyy hh:mm)\t (U) \n');   %Glucagon Bolus for Dual Closed Loop Only
  col_loc=3*(j-1)+2;
  l=1;
  location_glucagon_boluses = find(GluBol_D(:,col_loc)~=0);
  gluc_bolus_ind = GluBol_D(location_glucagon_boluses,col_loc);
  gluc_bolus_time_ind = GluBol_D(location_glucagon_boluses,col_loc-1);
  for pp = 1:length(gluc_bolus_ind)
        date_aux = datestr(gluc_bolus_time_ind(pp),'HH:MM');
        if str2num(date_aux(1,1:2)) >= 8 && str2num(date_aux(1,1:2)) <= 23                  %put the first date
            fprintf(fid,[date_D{1,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],gluc_bolus_ind(pp));
        else                                                                                %put the second date
            fprintf(fid,[date_D{2,j} ' ' date_aux(1,:) '\t %0.2f' '\n'],gluc_bolus_ind(pp));
        end
  end
  fprintf(fid,'\nInsulin_infusion ******************************************** \n');        %insulin infusion header 
  fprintf(fid,'Time \t\t\t Rate \n(dd/mm/yyyy hh:mm)\t (U/h) \n');
     for i=1:(length(InsInf_D{j})-1)
        if str2num(xtimestrI_D{j}(i,1:2)) >= 8 && str2num(xtimestrI_D{j}(i,1:2)) <= 23      %put the first date
            fprintf(fid,[date_D{1,j} ' ' xtimestrI_D{j}(i,:) '\t %0.2f' '\n'],InsInf_D{j}(i));
        else                                                                                %put the second date
            fprintf(fid,[date_D{2,j} ' ' xtimestrI_D{j}(i,:) '\t %0.2f' '\n'],InsInf_D{j}(i));
        end
     end
     if ~isempty(InsInf_D{j})
         fprintf(fid,[date_D{2,j} ' ' xtimestrI_D{j}(end,:) '\t %0.2f' '\n'],InsInf_D{j}(end)); %correction for last date
     end
  fprintf(fid,'\nGlucose_concentration ******************************************** \n');
  fprintf(fid,'Time \t\t\t Conc \n(dd/mm/yyyy hh:mm)\t (mmol/L) \n');
     for i=1:(length(GM_D{j})-1)
        if str2num(xtimestrGM_D{j}(i,1:2)) >= 8 && str2num(xtimestrGM_D{j}(i,1:2)) <= 23        %put the first date
            fprintf(fid,[date_D{1,j} ' ' xtimestrGM_D{j}(i,:) '\t %0.2f' '\n'],GM_D{j}(i));
        else                                                                                    %put the second date
            fprintf(fid,[date_D{2,j} ' ' xtimestrGM_D{j}(i,:) '\t %0.2f' '\n'],GM_D{j}(i));
        end
     end
     if ~isempty(GM_D{j})
         fprintf(fid,[date_D{2,j} ' ' xtimestrGM_D{j}(end,:) '\t %0.2f' '\n'],GM_D{j}(end));    %correction for last date
     end
  fprintf(fid,'\nReference_glucose_concentration ******************************************** \n');
  fprintf(fid,'Time \t\t\t Conc \n(dd/mm/yyyy hh:mm)\t (mmol/L) \n');
     for i=1:(length(BG_D{j})-1)
        if str2num(xtimestrBG_D{j}(i,1:2)) >= 8 && str2num(xtimestrBG_D{j}(i,1:2)) <= 23        %put the first date
            fprintf(fid,[date_D{1,j} ' ' xtimestrBG_D{j}(i,:) '\t %0.2f' '\n'],BG_D{j}(i));
        else                                                                                    %put the second date
            fprintf(fid,[date_D{2,j} ' ' xtimestrBG_D{j}(i,:) '\t %0.2f' '\n'],BG_D{j}(i));
        end
     end
     if ~isempty(BG_D{j})
         fprintf(fid,[date_D{2,j} ' ' xtimestrBG_D{j}(end,:) '\t %0.2f' '\n'],BG_D{j}(end));    %correction for last date
     end
     fprintf(fid,'\nPlasma_insulin_concentration ******************************************** \nTime \t\t\tconc \n(dd/mm/yyyy hh:mm)');
fprintf(fid,'\t(pmol/L) \n\nStart ******************************************** \nTime \n(dd/mm/yyyy hh:mm) \n');
fprintf(fid,[date_D{1,j} ' 08:00 \nEND']);
end
fprintf('Finished .txt files(dual). DONE \n')
toc
