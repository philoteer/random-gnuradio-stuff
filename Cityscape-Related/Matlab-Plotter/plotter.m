close all; clear all;
%File path
cscape_path = 'TEMPLE01/TEMPLE01.mat';

load(cscape_path);

%List of frequencies to plot.
f = [
    54,88;
    88,108;
    108,138;
    138,174;
    174,216;
    216,225;
    225,406;
    406,470;
    470,512;
    512,608;
    608,698;
    698,806;
    806,902;
    902,928;
    928,1000;
    1000,1240;
    1240,1300;
    1300,1400;
    1400,1525;
    1525,1710;
    1710,1850;
    1850,1990;
    1990,2110;
    2110,2200;
    2200,2300;
    2300,2360;
    2360,2390;
    2390,2500;
    2500,2686;
    2686,2900;
    2900,3000]';

%For each target frequency
for i=1:length(f)
  %plot
  plot(Freq,Avg)
  hold
  plot(Freq,Max_Hold,'g')
  xlim([f(1,i),f(2,i)])

  %label, title
  title(strcat('PSD Estimates From CityScape: from  ' , num2str(f(1,i)),' MHz to  ', num2str(f(2,i)),' MHz',' (',cscape_path,')'))
  ylabel('Power (dBm/24.4kHz)')
  xlabel('Frequency (MHz)')
  legend('Avg','MaxHold')

  %wait (optional; a workaround for a bug of Octave.)
  sleep(2)
  %save
  print (strcat(num2str(f(1,i)),'-',num2str(f(2,i)),'MHz'),'-dpng')

  close
  close all;
end
