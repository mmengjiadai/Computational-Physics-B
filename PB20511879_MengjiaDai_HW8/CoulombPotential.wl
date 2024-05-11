(* ::Package:: *)

BeginPackage["CoulombPotential`"]
(*delete previous definitions*)
Clear[WaveF,WaveR,WaveA]
(*declare functions,"usage" gives description*)
(*"_" is only used for function arguments*)
 WaveR::usage= "WaveR[Z_,r_,n_,l_]"
 WaveA::usage="WaveA[theta_,phi_,l_,m_]"
 WaveF::usage="WaveF[Z_,r_,theta_,phi_,n_,l_,m_]"
(*"Private" defines functions*)
(*the previous declarations make functions callable*)
Begin["`Private`"]
(*"Module works like functions in C programming language"*)
WaveR[Z_,r_,n_,l_]:=Module[{unit,tmp},unit=(1/(2l+1)!) Sqrt[(n+1)!/(2n (n-l-1)!)](((2Z)/n)^(l+3/2));  tmp=unit r^l Exp[-((Z r)/n)] Hypergeometric1F1[l+1-n,2l+2,(2Z r)/n]]
WaveA[theta_,phi_,l_,m_]:=Module[{tmp},tmp=SphericalHarmonicY[l,m,theta,phi];tmp]
WaveF[Z_,r_,theta_,phi_,n_,l_,m_]:=Module[{tmp},tmp=WaveR[Z,r,n,l] WaveA[theta,phi,l,m];tmp]
End[]
EndPackage[]
\[Placeholder]









