$# LS-DYNA Keyword file created by LS-PrePost(R) 2024/R2(4.11.3)-19Apr2024
$# Created on May-6-2025 (02:24:22)
*KEYWORD
*CONSTRAINED_EXTRA_NODES_SET
$#     pid      nsid     iflag
         8         1         0
*CONTACT_AUTOMATIC_GENERAL_ID
$#     cid                                                                 title
         1                                                                      
$#   surfa     surfb  surfatyp  surfbtyp   saboxid   sbboxid      sapr      sbpr
         2         0         2         0         0         0         0         0
$#      fs        fd        dc        vc       vdc    penchk        bt        dt
       0.3       0.2       0.0       0.0       0.0         0       0.01.00000E20
$#    sfsa      sfsb      sast      sbst     sfsat     sfsbt       fsf       vsf
       1.0       1.0       0.0       0.0       1.0       1.0       1.0       1.0
$#    soft    sofscl    lcidab    maxpar     sbopt     depth     bsort    frcfrq
         0       0.1         0     1.025         2         2         0         1
$#  penmax    thkopt    shlthk     snlog      isym     i2d3d    sldthk    sldstf
       0.0         0         0         0         0         0       0.0       0.0
$#    igap    ignore    dprfac    dtstif    unused    unused    flangl   cid_rcf
         1         0       0.0       0.0                           0.0         0
*SET_PART_LIST_TITLE
collision
$#     sid       da1       da2       da3       da4    solver
         2       0.0       0.0       0.0       0.0MECH
$#    pid1      pid2      pid3      pid4      pid5      pid6      pid7      pid8
         1         2         8         0         0         0         0         0
*CONTROL_CONTACT
$#  slsfac    rwpnal    islchk    shlthk    penopt    thkchg     orien    enmass
       0.1       1.0         2         0         1         1         2         1
$#  usrstr    usrfrc     nsbcs    interm     xpene     ssthk      ecdt   tiedprj
         0         0        10         0       4.0         0         0         0
$#   sfric     dfric       edc       vfc        th     th_sf    pen_sf     ptscl
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       1.0
$#  ignore    frceng   skiprwg    outseg   spotstp   spotdel   spothin   dir_tie
         1         0         0         0         0         0       0.0         0
$#    isym    nserod    rwgaps    rwgdth     rwksf      icov    swradf    ithoff
         0         0         1       0.0       1.0         0       1.0         0
$#  shledg    pstiff    ithcnt    tdcnof     ftall    unused    shltrw    igactc
         0         0         0         0         0                 0.0         0
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol
      50.0         0      0.01       0.01.000000E8         0
*CONTROL_TIMESTEP
$#  dtinit    tssfac      isdo    tslimt     dt2ms      lctm     erode     ms1st
1.00000E-6       0.0         0       0.0       0.0         0         0         0
*CONTROL_UNITS
$#  length      time      mass      temp
mm        ms        kg        k
*DATABASE_GLSTAT
$#      dt    binary      lcur     ioopt
       0.1         1         0         1
*DATABASE_MATSUM
$#      dt    binary      lcur     ioopt
       0.1         1         0         1
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid
       0.1         0         0         0         0
*DEFINE_TRANSFORMATION
$#  tranid
         1
$#  option        a1        a2        a3        a4        a5        a6        a7
TRANSL           0.0    -210.0      10.0       0.0       0.0       0.0       0.0
*INCLUDE_TRANSFORM
$#                                                                      filename
body_UAV.k
$#  idnoff    ideoff    idpoff    idmoff    idsoff    idfoff    iddoff
         0         0         0         0         0         0         0
$#  idroff         -    prefix    suffix
         0                              
$#  fctmas    fcttim    fctlen    fcttem   incout1    fctchg
       1.0       1.0       1.01.0                1       0.0
$#  tranid
         1
*INCLUDE_AUTO_OFFSET
$#                                                                      filename
adult_head_solid_single_spring.k
*INCLUDE_TRANSFORM
$#                                                                      filename
include_nose_cone_mesh.k
$#  idnoff    ideoff    idpoff    idmoff    idsoff    idfoff    iddoff
         0         0         0         0         0         0         0
$#  idroff         -    prefix    suffix
         0                              
$#  fctmas    fcttim    fctlen    fcttem   incout1    fctchg
       1.0       1.0       1.01.0                1       0.0
$#  tranid
         1
*END
