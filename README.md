# MC Sample Plots Generating Script

---

## Run

Run as follows: python3 plot.py


---

## Adjustable command-line arguments

- `--plotmode`  
  Choose which histogram(s) to plot:  
  `neg` = gen_pt == -50  
  `pos` = gen_pt != -50  
  `both` = both categories (default)

- `--maxfiles`  
  Number of input ROOT files to load (default: 1)

- `--var`  
  Which variable to plot by index (1–48) or `'all'` for all variables (default: `'all'`)

- `--log`  
  Plot y-axis on logarithmic scale (default: off)

- `--output_dir`  
  Output directory for saved plots (default: `plot_images_1`)

- `--x_min`  
  Minimum x-axis value (default: calculated automatically)

- `--x_max`  
  Maximum x-axis value (default: calculated automatically)

---

## Possible variables to plot

1. gen_eta         = generator-level (simulated) eta  
2. gen_phi         = generator-level (simulated) phi  
3. pt              = transverse momentum  
4. eta             = pseudorapidity  
5. phi             = azimuthal angle  
6. rawe            = raw energy  
7. pse             =   
8. ecorrerror      =   
9. sieie           = lateral shower-shape variable which measures spread of an electromagnetic shower in eta direction  
10. hoe            = hadron outer calorimeter energy?  
11. eiso           = ecal isolation value  
12. hiso           = hcal isolation value  
13. r9             = energy of 3x3 / energy of 5x5 supercluster, separates unconverted and converted photons  
14. smin_          =   
15. smaj           =   
16. detain         = the supercluster eta - track eta position at the PCA to the supercluster, extrapolated from the innermost track state  
17. dphiin         = the supercluster phi - track phi position at the PCA to the supercluster, extrapolated from the innermost track state  
18. ooemoop        =   
19. tiso           = tracker isolation value  
20. fbrem          = fraction of bremsstrahlung  
21. ieta           = integer index of HCAL barrel towers in eta dimension  
22. iphi           = integer index of HCAL barrel towers in phi dimension  
23. iseb           = barrel flag?  
24. eMax           = highest energy  
25. e2nd           = second highest energy  
26. eL             =   
27. eR             =   
28. eT             =   
29. eB             =   
30. e1x5           = energy deposition in 1x5 array of crystals around seed crystal  
31. e5x5           = energy deposition in 5x5 array of crystals around seed crystal  
32. e2x5M          =   
33. e2x5L          = energy deposition on the left of the 2x5 array of crystals around seed crystal  
34. e2x5R          = energy deposition on the right of the 2x5 array of crystals around seed crystal  
35. e2x5T          = energy deposition on the top of the 2x5 array of crystals around seed crystal  
36. e2x5B          = energy deposition on the bottom of the 2x5 array of crystals around seed crystal  
37. foundGoodTrack = whether or not a good track was found  
38. trkpt          = transverse momentum of the track  
39. trketa         = eta of the track  
40. trkphi         = phi of the track  
41. trkd0          = track in the x-y plane  
42. trkdz          = track along the beam axis  
43. trkq           = charge of the track  
44. trkpMode       = mode of the momentum of the track  
45. trketaMode     = mode of the eta of the track  
46. trkphiMode     = mode of the phi of the track  
47. trkqoverpModeError =   
48. trkchi2overndf = chi-squared over number of degrees of freedom of the track  

