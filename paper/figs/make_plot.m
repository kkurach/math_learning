
family_ind = 3;
save_plot = 0;
family = {'$(\sum (AA^T))_k$','$(\sum (A.*A)A^T))_k$','Sym$_k$','(RBM-1)$_k$','(RBM-2)$_k$'};

save_fname = {'sumAAT.pdf','multAAAT.pdf','sym.pdf','rbm1.pdf','rbm2.pdf'};

schedulers = {'TNN_dropout3','TNN_dropout8','NgramScheduler1','NgramScheduler2','NgramScheduler3','NgramScheduler4','NgramScheduler5','BruteForceScheduler'};
schedulers2 = {'TNN_{0.3}','TNN_{0.13}','1-gram','2-gram','3-gram','4-gram','5-gram','Random'};
cols = {'yx--' 'yx--' 'rx--' 'gx--' 'bx--' 'cx--' 'mx--' 'k:' };

max_k = 15;
offsets = 0*[-0.3:0.1:0.4]/20;

hits = zeros(length(schedulers),max_k-1);
h2=figure;
for i=1:length(schedulers)
    
    j=1;
    
    while exist(['times_',schedulers{i},'_',num2str(j)])
    
        tmp = eval(['times_',schedulers{i},'_',num2str(j)]);
  
        if (family_ind~=5)
            hits (i,:) = hits(i,:) + double(tmp(2:max_k)>-1);
        else
            tmp(tmp==-1)=600;
            hits (i,:,j) = double(tmp(2:max_k));    
        end
        j = j + 1;
        
    end
    
     if (family_ind~=5)
    hits(i,:) = hits(i,:) / (j-1);
     end
     
    if (i~=2)
        h=plot([2:max_k],hits(i,:)+offsets(i),cols{i},'Linewidth',2);  hold on;
    else
        plot([2:max_k],hits(i,:)+offsets(i),cols{i},'Color',[1 0.549 0],'Linewidth',2);  hold on;
    end
end

grid on;
xlabel('k','Fontsize',16)
ylabel('p(Success)','Fontsize',16)
h=legend(schedulers2,'Location','SouthWest');
set(h,'Fontsize',16);
set(gca,'XTick',[2:max_k]);
set(gca,'Fontsize',16);
axis([2 max_k 0 1]);
set(gcf,'Color','w');
title(family{family_ind},'Fontsize',16,'Interpreter','latex');

if save_plot
    export_fig(save_fname{family_ind});
end