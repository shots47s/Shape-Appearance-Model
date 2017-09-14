function [SmoSuf,s0,s1] = ComputeSmoSuf(f,a0,iphi,s)
% Smoothness and residuals stuff (not fully used)
% FORMAT [SmoSuf,s0,s1] = ComputeSmoSuf(f,a0,iphi,s)
%
% f      - Image
% a0     - Mean + linear combination of appearance bases
% iphi   - Deformation
% s      - Settings. Uses s.bs_args & s.likelihood
%
% SmoSuf - Stats for computing smoothness estimates
% s0     - Number of voxels
% s2     - Sum of squares residuals
%
% This bit of code is not fully used.
%__________________________________________________________________________
% Copyright (C) 2017 Wellcome Trust Centre for Neuroimaging

% John Ashburner
% $Id$

a1  = Resamp(a0,iphi,s.bs_args);
msk = all(isfinite(f),4) & all(isfinite(a1),4);
s0  = sum(msk(:));
d   = [size(a1) 1 1 1];
d   = d(1:4);

switch lower(s.likelihood)
case {'normal','gaussian','laplace'}
    res    = f-a1;
    for l=1:d(4)
        tmp   = res(:,:,:,l);
        s1(l) = sum(tmp(msk).^2);
    end
case {'binomial','binary'}
    sig    = 1./(1+exp(-a1));
    wt     = max(sig.*(1-sig),1e-3);
    res    = (f-sig);%./sqrt(wt);
    s1     = sum(res(msk(:)).^2);

case {'multinomial','categorical'}
    sig    = SoftMax(a1);
    res    = (f-sig);%./sqrt(max(sig.*(1-sig),1e-3));
    for l=1:d(4)
        tmp   = res(:,:,:,l);
        s1(l) = sum(tmp(msk).^2);
    end
end

% Compute sum of absolute gradients
SmoSuf    = zeros(1,8);
tmp       = res;
msk       = isfinite(tmp);
SmoSuf(1) = sum(msk(:));
%SmoSuf(2) = sum(abs(tmp(msk(:))));
SmoSuf(2) = sum(tmp(msk(:)).^2);

tmp       = res(2:end,:,:,:) - res(1:(end-1),:,:,:);
msk       = isfinite(tmp);
SmoSuf(3) = sum(msk(:));
%SmoSuf(4) = sum(abs(tmp(msk(:))));
SmoSuf(4) = sum(tmp(msk(:)).^2);

tmp       = res(:,2:end,:,:) - res(:,1:(end-1),:,:);
msk       = isfinite(tmp);
SmoSuf(5) = sum(msk(:));
%SmoSuf(6) = sum(abs(tmp(msk(:))));
SmoSuf(6) = sum(tmp(msk(:)).^2);

tmp       = res(:,:,2:end,:) - res(:,:,1:(end-1),:);
msk       = isfinite(tmp);
SmoSuf(7) = sum(msk(:));
%SmoSuf(8) = sum(abs(tmp(msk(:))));
SmoSuf(8) = sum(tmp(msk(:)).^2);

