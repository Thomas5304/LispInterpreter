techId(
 ( name      "Micronas" )
 ( version   2         )
 ( revision  0         )
);techId

controls(
techParams(
;( parameter           value )
;( ----------             ----- )
( maskGrid          0.05 )
( mask_grid         0.05 )
( scale             1 )
( mfgGrid           0.05 )
( drcGrid           0.05 )
( cadGrid           0.05 )
);techParams

viewTypeUnits(
;( viewType                userUnit        DBUPerUU )
;( --------                     --------           -- --------   )
  ( maskLayout		 micron 	1000	)
  ( schematic		 inch 	160	)
  ( schematicSymbol	 inch 	160	)
  ( netlist		 inch 	160	)
) ;viewTypeUnits

  mfgGridResolution(
    ( 0.05 )
  ) ;mfgGridResolution

leMPPControls (
; leMPPDefinition ( name           objList               spacings          masterIndex        [(exposedParameters)]) 
;                            ( -----             -------                ---------            ------------           ---------------------) 
leMPPDefinition ( psubGR	( ptypeGuardRing1xch )      ( 1 ) 	0 )

;leMPPRingObject (
;		name  masterPathName
;		enclosedPathNames
;		offsetPathNames
;		subRectangleNames
;		encShapeNames
;		netName
;		[exposedParameters]
;		-------------------------- )
leMPPRingObject (
		ptypeGuardRing1xch met1x1ch
		( diffEncPath pplusEncPath )
		nil 
		( defaultContacts )
		nil 
		vss!
		userParams( name netName )
);leMppRingObject

; leMPPDefinition ( name           objList               spacings          masterIndex        [(exposedParameters)]) 
;                            ( -----             -------                ---------            ------------           ---------------------) 
leMPPDefinition ( wellGR	( ntypeGuardRingch )      ( 1 ) 	0 )

;leMPPRingObject (
;		name  masterPathName
;		enclosedPathNames
;		offsetPathNames
;		subRectangleNames
;		encShapeNames
;		netName
;		[exposedParameters]
;		-------------------------- )
leMPPRingObject (
		ntypeGuardRingch pnwellx1
		( metEncwellch nwellEncPath )
		nil 
		( contswellx1 )
		nil 
		vdd!
		userParams( name netName )
);leMppRingObject

; leMPPDefinition ( name           objList               spacings          masterIndex        [(exposedParameters)]) 
;                            ( -----             -------                ---------            ------------           ---------------------) 
leMPPDefinition ( dwellGR	( ntypeGuardRingchdw )      ( 1 ) 	0 )

;leMPPRingObject (
;		name  masterPathName
;		enclosedPathNames
;		offsetPathNames
;		subRectangleNames
;		encShapeNames
;		netName
;		[exposedParameters]
;		-------------------------- )
leMPPRingObject (
		ntypeGuardRingchdw pnwellx1
		( metEncwellch dwellEncPath )
		nil 
		( contswellx1 )
		nil 
		vdd!
		userParams( name netName )
);leMppRingObject

; leMPPDefinition ( name           objList               spacings          masterIndex        [(exposedParameters)]) 
;                            ( -----             -------                ---------            ------------           ---------------------) 
leMPPDefinition ( phvwellGR	( phvwellRing1xch )      ( 1 ) 	0 )

;leMPPRingObject (
;		name  masterPathName
;		enclosedPathNames
;		offsetPathNames
;		subRectangleNames
;		encShapeNames
;		netName
;		[exposedParameters]
;		-------------------------- )
leMPPRingObject (
		phvwellRing1xch met1x1ch
		( diffEncPath pplusEncphv phvEncphv notfdnEncphv wellEncphv )
		nil 
		( defaultContacts )
		nil 
		vss!
		userParams( name netName )
);leMppRingObject

; leMPPDefinition ( name           objList               spacings          masterIndex        [(exposedParameters)]) 
;                            ( -----             -------                ---------            ------------           ---------------------) 
leMPPDefinition ( phvdwellGR	( phvwellRing1xchdw )      ( 1 ) 	0 )

;leMPPRingObject (
;		name  masterPathName
;		enclosedPathNames
;		offsetPathNames
;		subRectangleNames
;		encShapeNames
;		netName
;		[exposedParameters]
;		-------------------------- )
leMPPRingObject (
		phvwellRing1xchdw met1x1ch
		( diffEncPath pplusEncphv phvEncphv notfdnEncphv dwellEncphv )
		nil 
		( defaultContacts )
		nil 
		vss!
		userParams( name netName )
);leMppRingObject

;leMPPMasterPath (
;		name
;		layer   purpose
;		width   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPMasterPath (
		met1x1ch
		metal1   drawing
		1.1   extend t t
		userParams( name width layer purpose conn chop )
);leMPPMasterPath

;leMPPMasterPath (
;		name
;		layer   purpose
;		width   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPMasterPath (
		pnwellx1
		pn   drawing
		0.8   extend t nil
		userParams( name width layer purpose conn chop )
);leMPPMasterPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		metEncwellch
		metal1   drawing
		0.15  extend t t
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		diffEncPath
		pn   drawing
		0  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		pplusEncPath
		pplus   drawing
		0.4  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		pplusEncphv
		pplus   drawing
		0.7  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		phvEncphv
		phvwell   drawing
		1.05  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		notfdnEncphv
		notfdn   drawing
		0.55  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		wellEncphv
		well   drawing
		3.85  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		dwellEncphv
		dwell   drawing
		6.6  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		nwellEncPath
		well   drawing
		1.25  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPEnclosedPath (
;		name
;		layer   purpose
;		enclosure   pathStyle  conn   chop
;		[exposedParameters]
;		----------------------- )
leMPPEnclosedPath (
		dwellEncPath
		dwell   drawing
		1.05  extend t nil
		userParams( name enclosure layer purpose conn chop )
);leMPPEnclosedPath

;leMPPSubRect(
;		name
;		layer   purpose
;		width  height  conn   chop  enclosure  endOfLine   spacing   spacingType  numRows
;		[exposedParameters]
;		----------------------- )
leMPPSubRect (
		defaultContacts
		cut   drawing
		0.5   0.5 t t  0.3  0.3  0.5  fit  1
		userParams( name layer purpose width height conn chop minEnclosure eol spacing spaceType numRows )
);leMPPSubRect

;leMPPSubRect(
;		name
;		layer   purpose
;		width  height  conn   chop  enclosure  endOfLine   spacing   spacingType  numRows
;		[exposedParameters]
;		----------------------- )
leMPPSubRect (
		contswellx1
		cut   drawing
		0.5   0.5 t t  0.15  0.2  0.5  fit  1
		userParams( name layer purpose width height conn chop minEnclosure eol spacing spaceType numRows )
);leMPPSubRect

) ;leMPPControls

) ;controls

layerDefinitions(
 techPurposes(
;( purposeName  purposeNum   abbreviation )
;(   -----------        ----------        ----------     )
( keepout          19         KPO          )
( drawingA         20         dA           )
( drawingB         21         dB           )
( drawingC         22         dC           )
( drawingD         23         dD           )
( drawingE         24         dE           )
( dummy            25         dy           )
( dummyblock       26         dk           )
( halo             27         ho           )
( frozen           28         fn           )
( scratch          29         sh           )
( pn               30         pn           )
( poly1            31         poly1        )
( metal1           32         metal1       )
( metal2           33         metal2       )
( metal3           34         metal3       )
( poly0            35         poly0        )
( well             36         well         )
( dwell            37         dwell        )
( phvwell          38         phvwell      )
 ) ;techPurposes

 techLayers(
;( layerName  layerNum   abbreviation )
;(   ---------      --------      ------------ )
( boundary         0          boundar      )
( well             1          well         )
( pn               2          pn           )
( fdn              3          fdn          )
( absoutl          4          absoutl      )
( nimpl            5          nimpl        )
( poly1            6          poly1        )
( pimpl            7          pimpl        )
( cut              8          cut          )
( poly0            9          poly0        )
( metal1           10         metal1       )
( pass             11         pass         )
( via              12         via          )
( metal2           13         metal2       )
( outl             14         outl         )
( m60slot          15         m60slot      )
( m65slot          16         m65slot      )
( oxetch           17         oxetch       )
( cm               18         cm           )
( note             19         note         )
( notfdn           22         notfdn       )
( hvpn             23         hvpn         )
( hvwell           24         hvwell       )
( phvwell          25         phvwell      )
( swl              26         swl          )
( pdep             27         pdep         )
( dracer           30         dracer       )
( reticle          31         reticle      )
( arc              32         arc          )
( inr              33         inr          )
( pvt              34         pvt          )
( nvt              35         nvt          )
( jfetimp          36         jfetimp      )
( ldd2             37         ldd2         )
( ldd              38         ldd          )
( phimp            39         phimp        )
( fract            40         fract        )
( nonldd           41         nonldd       )
( p0etch           42         p0etch       )
( dwell            43         dwell        )
( rhi              44         rhi          )
( fgp              45         fgp          )
( ldd1             46         ldd1         )
( esd_impl         47         esd_imp      )
( oxn              48         oxn          )
( nonsilicide      49         nonsili      )
( esdw             50         esdw         )
( re               51         re           )
( bip              52         bip          )
( scl              53         scl          )
( ca               54         ca           )
( ax               55         ax           )
( splitwire        56         splitwi      )
( fract1           57         fract1       )
( ome1             58         ome1         )
( ome2             59         ome2         )
( tgme1            60         tgme1        )
( tgme2            61         tgme2        )
( scl1             62         scl1         )
( splitrp0         63         splitrp      )
( p1r              66         p1r          )
( p1c              67         p1c          )
( p2c              68         p2c          )
( bpl              69         bpl          )
( 5bd              70         5bd          )
( pgi              71         pgi          )
( pwell            72         pwell        )
( zero             73         zero         )
( draceref         74         dracere      )
( zimpl            75         zimpl        )
( ca_impl          76         ca_impl      )
( pplus            77         pplus        )
( notnplus         78         notnplus     )
( outline          79         outline      )
( polyptxt         80         polyptx      )
( met1ptxt         81         met1ptx      )
( met2ptxt         82         met2ptx      )
( polyinfo         83         polyinf      )
( met1info         84         met1inf      )
( met2info         85         met2inf      )
( physname         86         physnam      )
( tgpol            87         tgpol        )
( conpol           88         conpol       )
( conme1           89         conme1       )
( conme2           90         conme2       )
( boutl1           91         blockou      )
( boutl2           92         blockou      )
( uc               93         uc           )
( imPlace          94         imPlace      )
( dhvwell          95         dhvwell      )
( onetch           96         onetch       )
( sfgate           97         sfgate       )
( m65nosl          98         m65nosl      )
( idtext           99         idtext       )
( CRX              100        CRX          )
( CRY              101        CRY          )
( ERR              102        ERR          )
( UC               103        UC           )
( RUL              104        RUL          )
( RSLV             105        RSLV         )
( NTRAN            106        NTRAN        )
( PTRAN            107        PTRAN        )
( via2             108        via2         )
( metal3           109        metal3       )
( antdio           113        antdio       )
( switch           114        switch       )
( p0etchST         115        p0etchST     )
( polyimid         116        polyimid     )
( rom              117        rom          )
( pwellblk         118        pwellblk     )
( polgapblk        119        polgapblk    )
( znanode          120        znanode      )
( pco_blk          121        pco_blk      )
( re_m3            122        re_m3        )
( prgtetch         123        prgtetch     )
( vtblock          124        vtblock      )
( hallwell         125        hallwell     )
( trench           126        trench       )
( guardRing        127        guardRing    )
( pCell            128        pCell        )
( chipBoundary     129        chipBndr     )
( OpCaEtch         130        OpCaEtch     )
( PNCaEtch         131        PNCaEtch     )
( OxCaEtch         132        OxCaEtch     )
( subreg           133        subreg       )
( vtpa             134        vtpa         )
( DMYBLKpoly1      135        DMYBLKp1     )
( DMYBLKmetal1     136        DMYBLKm1     )
( DMYBLKmetal2     137        DMYBLKm2     )
( DMYBLKmetal3     138        DMYBLKm3     )
( PRBLKpoly1       139        PRBLKp1      )
( PRBLKmetal1      140        PRBLKm1      )
( PRBLKmetal2      141        PRBLKm2      )
( PRBLKmetal3      142        PRBLKm3      )
( BSD              143        BSD          )
( SuspendedGate    144        SG           )
( re_m2            145        re_m2        )
( customviamarker  146	      customviamarker          )
( subregicv        147        subregicv    )
( lowvoltage       148        lowvt        )
 ) ;techLayers

 techLayerPurposePriorities(
;(  layerName   purposeName  )
;(   ---------        ------------     )
( background       drawing          )
( pplus            pin              )
( text             label            )
( well             pin              )
( boundary         drawing          )
( ldd1             drawing          )
( ldd              drawing          )
( ldd2             drawing          )
( reticle          drawing          )
( fract            drawing          )
( fract1           drawing          )
( esdw             drawing          )
( bip              drawing          )
( pn               drawing          )
( hvpn             drawing          )
( well             drawing          )
( dwell            drawing          )
( hvwell           drawing          )
( dhvwell          drawing          )
( phvwell          drawing          )
( BSD              drawing          )
( hallwell         drawing          )
( fdn              drawing          )
( notfdn           drawing          )
( arc              drawing          )
( inr              drawing          )
( fgp              drawing          )
( oxn              drawing          )
( poly1            drawing          )
( p1r              drawing          )
( p1c              drawing          )
( swl              drawing          )
( pdep             drawing          )
( pvt              drawing          )
( nvt              drawing          )
( vtblock          drawing          )
( trench           drawing          )
( vtpa             drawing          )
( jfetimp          drawing          )
( phimp            drawing          )
( sfgate           drawing          )
( nonldd           drawing          )
( pimpl            drawing          )
( pplus            drawing          )
( nimpl            drawing          )
( notnplus         drawing          )
( rhi              drawing          )
( poly0            drawing          )
( p2c              drawing          )
( esd_impl         drawing          )
( zimpl            drawing          )
( znanode          drawing          )
( ca_impl          drawing          )
( cm               drawing          )
( nonsilicide      drawing          )
( metal1           drawing          )
( via              drawing          )
( metal2           drawing          )
( via2             drawing          )
( metal3           drawing          )
( cut              drawing          )
( pass             drawing          )
( polyimid         drawing          )
( oxetch           drawing          )
( p0etch           drawing          )
( p0etchST         drawing          )
( onetch           drawing          )
( OpCaEtch         drawing          )
( PNCaEtch         drawing          )
( OxCaEtch         drawing          )
( prgtetch         drawing          )
( ax               drawing          )
( scl1             drawing          )
( scl              drawing          )
( ca               drawing          )
( re               drawing          )
( re_m2            drawing          )
( re_m3            drawing          )
( re               pn               )
( re               poly1            )
( re               metal1           )
( re               metal2           )
( re               metal3           )
( re               poly0            )
( re               well             )
( re               dwell            )
( re               phvwell          )
( m65nosl          drawing          )
( splitrp0         drawing          )
( splitwire        drawing          )
( antdio           drawing          )
( switch           drawing          )
( pco_blk          drawing          )
( DMYBLKpoly1      drawing          )
( DMYBLKmetal1     drawing          )
( DMYBLKmetal2     drawing          )
( DMYBLKmetal3     drawing          )
( PRBLKpoly1       drawing          )
( PRBLKmetal1      drawing          )
( PRBLKmetal2      drawing          )
( PRBLKmetal3      drawing          )
( note             label            )
( SuspendedGate    drawing          )
( pn               pin              )
( poly1            pin              )
( metal1           pin              )
( metal2           pin              )
( metal3           pin              )
( pn               label            )
( poly1            label            )
( metal1           label            )
( metal2           label            )
( metal3           label            )
( poly1            dummy            )
( metal1           dummy            )
( metal2           dummy            )
( metal3           dummy            )
( poly1            dummyblock       )
( metal1           dummyblock       )
( metal2           dummyblock       )
( metal3           dummyblock       )
( bpl              drawing          )
( 5bd              drawing          )
( pgi              drawing          )
( pwell            drawing          )
( zero             drawing          )
( dracer           drawing          )
( dracer           drawing1         )
( dracer           drawing2         )
( dracer           drawing3         )
( dracer           drawing4         )
( dracer           drawing5         )
( dracer           drawing6         )
( dracer           drawing7         )
( dracer           drawing8         )
( dracer           drawing9         )
( dracer           drawingA         )
( dracer           drawingB         )
( dracer           drawingC         )
( dracer           drawingD         )
( dracer           drawingE         )
( draceref         drawing          )
( outline          label            )
( metal1           boundary         )
( ome1             drawing          )
( ome2             drawing          )
( tgpol            drawing          )
( tgme1            drawing          )
( tgme2            drawing          )
( conpol           drawing          )
( conme1           drawing          )
( conme2           drawing          )
( conpol           label            )
( conme1           label            )
( conme2           label            )
( polyptxt         label            )
( met1ptxt         label            )
( met2ptxt         label            )
( polyinfo         label            )
( met1info         label            )
( met2info         label            )
( physname         label            )
( absoutl          drawing          )
( absoutl          label            )
( boutl1           drawing          )
( boutl2           drawing          )
( uc               drawing          )
( outl             drawing          )
( m60slot          drawing          )
( m65slot          drawing          )
( poly1            keepout          )
( metal1           keepout          )
( metal2           keepout          )
( metal3           keepout          )
( CRX              drawing          )
( CRY              drawing          )
( ERR              drawing          )
( UC               drawing          )
( RUL              drawing          )
( RSLV             drawing          )
( NTRAN            drawing          )
( PTRAN            drawing          )
( imPlace          drawing          )
( imPlace          drawing1         )
( imPlace          label            )
( guardRing        halo             )
( guardRing        keepout          )
( guardRing        scratch          )
( pCell            frozen           )
( pCell            pin              )
( rom              drawing          )
( pwellblk         drawing          )
( polgapblk        drawing          )
( chipBoundary     drawing          )
( idtext           label            )
( subreg           drawing          )
( subregicv        drawing          )
( lowvoltage       drawing          )
( annotate         drawing          )
( annotate         drawing1         )
( annotate         drawing2         )
( annotate         drawing3         )
( annotate         drawing4         )
( annotate         drawing5         )
( annotate         drawing6         )
( annotate         drawing7         )
( annotate         drawing8         )
( annotate         drawing9         )
( axis             drawing          )
( device           annotate         )
( device           drawing          )
( device           drawing1         )
( device           drawing2         )
( device           label            )
( grid             drawing          )
( grid             drawing1         )
( hilite           drawing          )
( hilite           drawing1         )
( hilite           drawing2         )
( hilite           drawing3         )
( hilite           drawing4         )
( hilite           drawing5         )
( hilite           drawing6         )
( hilite           drawing7         )
( hilite           drawing8         )
( hilite           drawing9         )
( instance         drawing          )
( instance         label            )
( pin              annotate         )
( pin              drawing          )
( pin              label            )
( prBoundary       drawing          )
( text             drawing          )
( text             drawing1         )
( text             drawing2         )
( wire             drawing          )
( wire             flight           )
( wire             label            )
( customviamarker  drawing          )
) ;techLayerPurposePriorities

techDisplays(
;(lLayerName purposeName  packet  vis sel   con2ChgLy   drgEnbl  valid )
;(   ---------        -------           ------   --- ---    ------------     -------    ----- )
( background       drawing          P_background_drawing	t nil t nil nil  )
( pplus            pin              pplus_pin       	t t nil nil t  )
( text             label            text_label      	t t nil nil t  )
( well             pin              well_pin        	t t nil nil t  )
( boundary         drawing          P_boundary_drawing	t t t t t  )
( ldd1             drawing          P_ldd1_drawing  	t t t t t  )
( ldd              drawing          P_ldd_drawing   	t t t t t  )
( ldd2             drawing          P_ldd2_drawing  	t t t t t  )
( reticle          drawing          P_reticle_drawing	t t t t t  )
( fract            drawing          P_fract_drawing 	t t t t t  )
( fract1           drawing          P_fract1_drawing	t t t t t  )
( esdw             drawing          P_esdw_drawing  	t t t t t  )
( bip              drawing          P_bip_drawing   	t t t t t  )
( pn               drawing          P_pn_drawing    	t t t t t  )
( hvpn             drawing          P_hvpn_drawing  	t t t t t  )
( well             drawing          P_well_drawing  	t t t t t  )
( dwell            drawing          P_dwell_drawing 	t t t t t  )
( hvwell           drawing          P_hvwell_drawing	t t t t t  )
( dhvwell          drawing          P_dhvwell_drawing	t t t t t  )
( phvwell          drawing          P_phvwell_drawing	t t t t t  )
( BSD              drawing          defaultPacket   	t t nil nil t  )
( hallwell         drawing          P_hallwell_drawing	t t t t t  )
( fdn              drawing          P_fdn_drawing   	t t t t t  )
( notfdn           drawing          P_notfdn_drawing	t t t t t  )
( arc              drawing          P_arc_drawing   	t t t t t  )
( inr              drawing          P_inr_drawing   	t t t t t  )
( fgp              drawing          P_fgp_drawing   	t t t t t  )
( oxn              drawing          P_oxn_drawing   	t t t t t  )
( poly1            drawing          P_poly1_drawing 	t t t t t  )
( p1r              drawing          P_p1r_drawing   	t t t t t  )
( p1c              drawing          P_p1c_drawing   	t t t t t  )
( swl              drawing          P_swl_drawing   	t t t t t  )
( pdep             drawing          P_pdep_drawing  	t t t t t  )
( pvt              drawing          P_pvt_drawing   	t t t t t  )
( nvt              drawing          P_nvt_drawing   	t t t t t  )
( vtblock          drawing          P_vtblock_drawing	t t t t t  )
( trench           drawing          P_trench_drawing	t t t t t  )
( vtpa             drawing          P_vtpa_drawing  	t t t t t  )
( jfetimp          drawing          P_jfetimp_drawing	t t t t t  )
( phimp            drawing          P_phimp_drawing 	t t t t t  )
( sfgate           drawing          P_sfgate_drawing	t t t t t  )
( nonldd           drawing          P_nonldd_drawing	t t t t t  )
( pimpl            drawing          P_pimpl_drawing 	t t t t t  )
( pplus            drawing          P_pplus_drawing 	t t t t t  )
( nimpl            drawing          P_nimpl_drawing 	t t t t t  )
( notnplus         drawing          P_notnplus_drawing	t t t t t  )
( rhi              drawing          P_rhi_drawing   	t t t t t  )
( poly0            drawing          P_poly0_drawing 	t t t t t  )
( p2c              drawing          P_p2c_drawing   	t t t t t  )
( esd_impl         drawing          P_esd_impl_drawing	t t t t t  )
( zimpl            drawing          P_zimpl_drawing 	t t t t t  )
( znanode          drawing          P_znanode_drawing	t t t t t  )
( ca_impl          drawing          P_ca_impl_drawing	t t t t t  )
( cm               drawing          P_cm_drawing    	t t t t t  )
( nonsilicide      drawing          P_nonsilicide_drawing	t t t t t  )
( metal1           drawing          P_metal1_drawing	t t t t t  )
( via              drawing          P_via_drawing   	t t t t t  )
( metal2           drawing          P_metal2_drawing	t t t t t  )
( via2             drawing          P_via2_drawing  	t t t t t  )
( metal3           drawing          P_metal3_drawing	t t t t t  )
( cut              drawing          P_cut_drawing   	t t t t t  )
( pass             drawing          P_pass_drawing  	t t t t t  )
( polyimid         drawing          P_polyimid_drawing	t t t t t  )
( oxetch           drawing          P_oxetch_drawing	t t t t t  )
( p0etch           drawing          P_p0etch_drawing	t t t t t  )
( p0etchST         drawing          P_p0etchST_drawing	t t t t t  )
( onetch           drawing          P_onetch_drawing	t t t t t  )
( OpCaEtch         drawing          P_OpCaEtch_drawing	t t t t t  )
( PNCaEtch         drawing          P_PNCaEtch_drawing	t t t t t  )
( OxCaEtch         drawing          P_OxCaEtch_drawing	t t t t t  )
( prgtetch         drawing          P_prgtetch_drawing	t t t t t  )
( ax               drawing          P_ax_drawing    	t t t t t  )
( scl1             drawing          P_scl1_drawing  	t t t t t  )
( scl              drawing          P_scl_drawing   	t t t t t  )
( ca               drawing          P_ca_drawing    	t t t t t  )
( re               drawing          P_re_drawing    	t t t t t  )
( re               pn               P_re_drawing    	t t t t t  )
( re               poly1            P_re_drawing    	t t t t t  )
( re               metal1           P_re_drawing    	t t t t t  )
( re               well             P_re_drawing    	t t t t t  )
( re               dwell            P_re_drawing    	t t t t t  )
( re               phvwell          P_re_drawing    	t t t t t  )
( re               metal2           P_re_m2_drawing     t t t t t  )
( re               metal3           P_re_m3_drawing 	t t t t t  )
( re_m2            drawing          P_re_m2_drawing     t t t t t  )
( re_m3            drawing          P_re_m3_drawing 	t t t t t  )
( re               poly0            P_re_drawing    	t t t t t  )
( m65nosl          drawing          P_m65nosl_drawing	t t t t t  )
( splitrp0         drawing          P_splitrp0_drawing	t t t t t  )
( splitwire        drawing          P_splitwire_drawing	t t t t t  )
( antdio           drawing          P_antdio_drawing	t t t t t  )
( switch           drawing          P_switch_drawing	t t t t t  )
( pco_blk          drawing          P_pco_blk_drawing	t t t t t  )
( DMYBLKpoly1      drawing          P_DMYBLKpoly1_drawing	t t t nil t  )
( DMYBLKmetal1     drawing          P_DMYBLKmetal1_drawing	t t t nil t  )
( DMYBLKmetal2     drawing          P_DMYBLKmetal2_drawing	t t t nil t  )
( DMYBLKmetal3     drawing          P_DMYBLKmetal3_drawing	t t t nil t  )
( PRBLKpoly1       drawing          P_PRBLKpoly1_drawing	t t t nil t  )
( PRBLKmetal1      drawing          P_PRBLKmetal1_drawing	t t t nil t  )
( PRBLKmetal2      drawing          P_PRBLKmetal2_drawing	t t t nil t  )
( PRBLKmetal3      drawing          P_PRBLKmetal3_drawing	t t t nil t  )
( note             label            P_note_label    	t t t nil t  )
( SuspendedGate    drawing          defaultPacket   	t t nil nil t  )
( pn               pin              P_pn_pin        	t t t t t  )
( poly1            pin              P_poly1_pin     	t t t t t  )
( metal1           pin              P_metal1_pin    	t t t t t  )
( metal2           pin              P_metal2_pin    	t t t t t  )
( metal3           pin              P_metal3_pin    	t t t t t  )
( pn               label            P_pn_label      	t t t nil t  )
( poly1            label            P_poly1_label   	t t t nil t  )
( metal1           label            P_metal1_label  	t t t nil t  )
( metal2           label            P_metal2_label  	t t t nil t  )
( metal3           label            P_metal3_label  	t t t nil t  )
( poly1            dummy            P_polydpat_drawing	t t t nil t  )
( metal1           dummy            P_met1dpat_drawing	t t t nil t  )
( metal2           dummy            P_met2dpat_drawing	t t t nil t  )
( metal3           dummy            P_met3dpat_drawing	t t t nil t  )
( poly1            dummyblock       P_dont_use	t t t nil t  )
( metal1           dummyblock       P_dont_use	t t t nil t  )
( metal2           dummyblock       P_dont_use	t t t nil t  )
( metal3           dummyblock       P_dont_use	t t t nil t  )
( bpl              drawing          P_bpl_drawing   	t t t t t  )
( 5bd              drawing          P_5bd_drawing   	t t t t t  )
( pgi              drawing          P_pgi_drawing   	t t t t t  )
( pwell            drawing          P_pwell_drawing 	t t t t t  )
( zero             drawing          P_zero_drawing  	t t t t t  )
( dracer           drawing          P_dracer_drawing	t t t t t  )
( dracer           drawing1         P_dracer_drawing1	t t t t t  )
( dracer           drawing2         P_dracer_drawing2	t t t t t  )
( dracer           drawing3         P_dracer_drawing3	t t t t t  )
( dracer           drawing4         P_dracer_drawing4	t t t t t  )
( dracer           drawing5         P_dracer_drawing5	t t t t t  )
( dracer           drawing6         P_dracer_drawing6	t t t t t  )
( dracer           drawing7         P_dracer_drawing7	t t t t t  )
( dracer           drawing8         P_dracer_drawing8	t t t t t  )
( dracer           drawing9         P_dracer_drawing9	t t t t t  )
( dracer           drawingA         P_actarea_drawing	t t t t t  )
( dracer           drawingB         P_gatepoly_drawing	t t t t t  )
( dracer           drawingC         P_contact_drawing	t t t t t  )
( dracer           drawingD         P_via1_drawing  	t t t t t  )
( dracer           drawingE         P_via2_drawing  	t t t t t  )
( draceref         drawing          P_draceref_drawing	t t t t t  )
( outline          label            P_outline_label 	t t t nil t  )
( metal1           boundary         P_metal1_boundary	t t t t nil  )
( ome1             drawing          P_ome1_drawing  	t t t t t  )
( ome2             drawing          P_ome2_drawing  	t t t t t  )
( tgpol            drawing          P_tgpol_drawing 	t t t t t  )
( tgme1            drawing          P_tgme1_drawing 	t t t t t  )
( tgme2            drawing          P_tgme2_drawing 	t t t t t  )
( conpol           drawing          P_conpol_drawing	t t t t t  )
( conme1           drawing          P_conme1_drawing	t t t t t  )
( conme2           drawing          P_conme2_drawing	t t t t t  )
( conpol           label            P_conpol_drawing	t t t nil t  )
( conme1           label            P_conme1_drawing	t t t nil t  )
( conme2           label            P_conme2_drawing	t t t nil t  )
( polyptxt         label            P_polyptxt_label	t t t nil t  )
( met1ptxt         label            P_met1ptxt_label	t t t nil t  )
( met2ptxt         label            P_met2ptxt_label	t t t nil t  )
( polyinfo         label            P_polyinfo_label	t t t nil t  )
( met1info         label            P_met1info_label	t t t nil t  )
( met2info         label            P_met2info_label	t t t nil t  )
( physname         label            P_physname_label	t t t nil t  )
( absoutl          drawing          P_absoutl_drawing	t t t t t  )
( absoutl          label            P_absoutl_label 	t t t nil t  )
( boutl1           drawing          P_boutl1_drawing	t t t t t  )
( boutl2           drawing          P_boutl2_drawing	t t t t t  )
( uc               drawing          P_uc_drawing    	t t t t t  )
( outl             drawing          P_outl_drawing  	t t t t t  )
( m60slot          drawing          P_m60slot_drawing	t t t t t  )
( m65slot          drawing          P_m65slot_drawing	t t t t t  )
( poly1            keepout          P_dont_use	t t t nil t  )
( metal1           keepout          P_dont_use	t t t nil t  )
( metal2           keepout          P_dont_use	t t t nil t  )
( metal3           keepout          P_dont_use	t t t nil t  )
( CRX              drawing          P_CRX_drawing   	t t t t t  )
( CRY              drawing          P_CRY_drawing   	t t t t t  )
( ERR              drawing          P_ERR_drawing   	t t t t t  )
( UC               drawing          P_UC_drawing    	t t t t t  )
( RUL              drawing          P_RUL_drawing   	t t t t t  )
( RSLV             drawing          P_RSLV_drawing  	t t t t t  )
( NTRAN            drawing          P_NTRAN_drawing 	t t t t t  )
( PTRAN            drawing          P_PTRAN_drawing 	t t t t t  )
( imPlace          drawing          P_imPlace_drawing	t t t t t  )
( imPlace          drawing1         P_imPlace_drawing1	t t t t t  )
( imPlace          label            P_imPlace_drawing	t t t nil t  )
( guardRing        halo             P_guardRing_halo	t t t t t  )
( guardRing        keepout          P_guardRing_keepout	t t t t t  )
( guardRing        scratch          P_guardRing_scratch	t t t t t  )
( pCell            frozen           P_pCell_frozen  	t t t t t  )
( pCell            pin              P_pCell_pin     	nil nil nil nil nil  )
( rom              drawing          P_rom_drawing   	t t t t t  )
( pwellblk         drawing          P_pwellblk_drawing	t t t t t  )
( polgapblk        drawing          P_polgapblk_drawing	t t t t t  )
( chipBoundary     drawing          P_chipBoundary_drawing	t t t t t  )
( idtext           label            P_idtext_label  	t t t t t  )
( subreg           drawing          P_subreg_drawing	nil nil t nil nil  )
( subregicv        drawing          P_subreg_drawing	t t t t t  )
( lowvoltage       drawing          P_lowvoltage_drawing	t t t t t  )
( annotate         drawing          P_annotate_drawing	t t t t nil  )
( annotate         drawing1         P_annotate_drawing1	t t t t nil  )
( annotate         drawing2         P_annotate_drawing2	t t t t nil  )
( annotate         drawing3         P_annotate_drawing3	t t t t nil  )
( annotate         drawing4         P_annotate_drawing4	t t t t nil  )
( annotate         drawing5         P_annotate_drawing5	t t t t nil  )
( annotate         drawing6         P_annotate_drawing6	t t t t nil  )
( annotate         drawing7         P_annotate_drawing7	t t t t nil  )
( annotate         drawing8         P_annotate_drawing8	t t t t nil  )
( annotate         drawing9         P_annotate_drawing9	t t t t nil  )
( axis             drawing          P_axis_drawing  	t nil t t nil  )
( device           annotate         P_device_annotate	t t t t nil  )
( device           drawing          P_device_drawing	t t t t nil  )
( device           drawing1         P_device_drawing1	t t t t nil  )
( device           drawing2         P_device_drawing2	t t t t nil  )
( device           label            P_device_label  	t t t t nil  )
( grid             drawing          P_grid_drawing  	t nil t nil nil  )
( grid             drawing1         P_grid_drawing1 	t nil t nil nil  )
( hilite           drawing          P_hilite_drawing	t t t t nil  )
( hilite           drawing1         P_hilite_drawing1	t t t t nil  )
( hilite           drawing2         P_hilite_drawing2	t t t t nil  )
( hilite           drawing3         P_hilite_drawing3	t t t t nil  )
( hilite           drawing4         P_hilite_drawing4	t t t t nil  )
( hilite           drawing5         P_hilite_drawing5	t t t t nil  )
( hilite           drawing6         P_hilite_drawing6	t t t t nil  )
( hilite           drawing7         P_hilite_drawing7	t t t t nil  )
( hilite           drawing8         P_hilite_drawing8	t t t t nil  )
( hilite           drawing9         P_hilite_drawing9	t t t t nil  )
( instance         drawing          P_instance_drawing	t t t t nil  )
( instance         label            P_instance_label	t t t t nil  )
( pin              annotate         P_pin_annotate  	t t t t nil  )
( pin              drawing          P_pin_drawing   	t t t t nil  )
( pin              label            P_pin_label     	t t t t nil  )
( prBoundary       drawing          P_prBoundary_drawing	t t t t t  )
( text             drawing          P_text_drawing  	t t t t nil  )
( text             drawing1         P_text_drawing1 	t t t t nil  )
( text             drawing2         P_text_drawing2 	t t t t nil  )
( wire             drawing          P_wire_drawing  	t t t t nil  )
( wire             flight           P_wire_flight   	t t t t nil  )
( wire             label            P_wire_label    	t t t t nil  )
( customviamarker  drawing          P_customviamarker_drawing nil nil t nil nil)
) ;techDisplays

;; techDerivedLayers(
;; ;( DerivedLayerName          #          composition  )
;; ;( ----------------          ------     ------------ )
;;  ( dGate       	10001           ( AND poly1 	   pn     ))
;;  ( dDiffInNwell       	10002           ( AND pn    	   well   ))
;;  ( dDiffOutNwell       10003           ( NOT pn    	   well   ))
;;  ( dPSD       		10004           ( AND dDiffInNwell pplus  ))
;; ) ;techDerivedLayers

) ;layerDefinitions

layerRules(
 functions(
;( layer     function     [maskNumber])
;( -----      --------        ------------    )
( well              nWell         1 )
( pn                diffusion     2 )
( poly1             poly          8 )
( cut               cut           9 )
( metal1            metal         10 )
( via               cut           12 )
( metal2            metal         13 )
( via2              cut           21 )
( metal3            metal         22 )
 ) ;functions

 mfgResolutions(
;( layer         mfgResolution )
;( -----           -------------    )
( boundary           0.05 )
( well               0.05 )
( pn                 0.05 )
( fdn                0.05 )
( absoutl            0.05 )
( nimpl              0.05 )
( poly1              0.05 )
( pimpl              0.05 )
( cut                0.05 )
( poly0              0.05 )
( metal1             0.05 )
( pass               0.05 )
( via                0.05 )
( metal2             0.05 )
( outl               0.05 )
( m60slot            0.05 )
( m65slot            0.05 )
( oxetch             0.05 )
( cm                 0.05 )
( note               0.05 )
( notfdn             0.05 )
( hvpn               0.05 )
( hvwell             0.05 )
( phvwell            0.05 )
( swl                0.05 )
( pdep               0.05 )
( dracer             0.05 )
( reticle            0.05 )
( arc                0.05 )
( inr                0.05 )
( pvt                0.05 )
( nvt                0.05 )
( jfetimp            0.05 )
( ldd2               0.05 )
( ldd                0.05 )
( phimp              0.05 )
( fract              0.05 )
( nonldd             0.05 )
( p0etch             0.05 )
( dwell              0.05 )
( rhi                0.05 )
( fgp                0.05 )
( ldd1               0.05 )
( esd_impl           0.05 )
( oxn                0.05 )
( nonsilicide        0.05 )
( esdw               0.05 )
( re                 0.05 )
( re_m2              0.05 )
( re_m3              0.05 )
( bip                0.05 )
( scl                0.05 )
( ca                 0.05 )
( ax                 0.05 )
( splitwire          0.05 )
( fract1             0.05 )
( ome1               0.05 )
( ome2               0.05 )
( tgme1              0.05 )
( tgme2              0.05 )
( scl1               0.05 )
( splitrp0           0.05 )
( p1r                0.05 )
( p1c                0.05 )
( p2c                0.05 )
( bpl                0.05 )
( 5bd                0.05 )
( pgi                0.05 )
( pwell              0.05 )
( zero               0.05 )
( draceref           0.05 )
( zimpl              0.05 )
( ca_impl            0.05 )
( pplus              0.05 )
( notnplus           0.05 )
( outline            0.05 )
( polyptxt           0.05 )
( met1ptxt           0.05 )
( met2ptxt           0.05 )
( polyinfo           0.05 )
( met1info           0.05 )
( met2info           0.05 )
( physname           0.05 )
( tgpol              0.05 )
( conpol             0.05 )
( conme1             0.05 )
( conme2             0.05 )
( boutl1             0.05 )
( boutl2             0.05 )
( uc                 0.05 )
( imPlace            0.05 )
( dhvwell            0.05 )
( onetch             0.05 )
( sfgate             0.05 )
( m65nosl            0.05 )
( idtext             0.05 )
( CRX                0.05 )
( CRY                0.05 )
( ERR                0.05 )
( UC                 0.05 )
( RUL                0.05 )
( RSLV               0.05 )
( NTRAN              0.05 )
( PTRAN              0.05 )
( via2               0.05 )
( metal3             0.05 )
( antdio             0.05 )
( switch             0.05 )
( p0etchST           0.05 )
( polyimid           0.05 )
( rom                0.05 )
( pwellblk           0.05 )
( polgapblk          0.05 )
( znanode            0.05 )
( pco_blk            0.05 )
( prgtetch           0.05 )
( vtblock            0.05 )
( hallwell           0.05 )
( trench             0.05 )
( guardRing          0.05 )
( pCell              0.05 )
( chipBoundary       0.05 )
( OpCaEtch           0.05 )
( PNCaEtch           0.05 )
( OxCaEtch           0.05 )
( subreg             0.05 )
( subregicv          0.05 )
( lowvoltage         0.05 )
( vtpa               0.05 )
( DMYBLKpoly1        0.05 )
( DMYBLKmetal1       0.05 )
( DMYBLKmetal2       0.05 )
( DMYBLKmetal3       0.05 )
( PRBLKpoly1         0.05 )
( PRBLKmetal1        0.05 )
( PRBLKmetal2        0.05 )
( PRBLKmetal3        0.05 )
( BSD                0.05 )
( SuspendedGate      0.05 )
( customviamarker    0.05 )
 ) ;mfgResolutions

) ;layerRules

 viaDefs(
standardViaDefs(
;(viaDefName  layer1  layer2  (cutLayer cutWidth cutHeight [resistancePerCut])
;(cutRows   cutCol  (cutSpacing))
;(layer1Enc) (layer2Enc) (layer1Offset)  (layer2Offset)  (origOffset)
;[implant1   (implant1Enc)  [implant2  (implant2Enc)]])
;( -------------------------------------------------------------------------- )
(M1_POLY1         poly1        metal1       ( cut         0.5 0.5 0 ) 
 (1 1 ( 0.5 0.5 )  )
 ( 0.3 0.3 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 )  )
(M2_M1         metal1        metal2       ( via         0.55 0.55 0 ) 
 (1 1 ( 0.5 0.5 )  )
 ( 0.3 0.3 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 )  )
(M3_M2         metal2        metal3       ( via2         0.6 0.6 0 ) 
 (1 1 ( 0.55 0.55 )  )
 ( 0.3 0.3 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 )  )
(M1_ND            pn           metal1       ( cut         0.5 0.5 0 ) 
 (1 1 ( 0.5 0.5 )  )
 ( 0.15 0.15 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 )  )
(M1_PD            pn           metal1       ( cut         0.5 0.5 0 ) 
 (1 1 ( 0.5 0.5 )  )
 ( 0.3 0.3 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) 
pplus         ( 0.7 0.7 )  )
(M1_wellcon       pn           metal1       ( cut         0.5 0.5 0 ) 
 (1 1 ( 0.5 0.5 )  )
 ( 0.25 0.25 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) 
well          ( 0.4 0.4 )  )
(M1_subcon        pn           metal1       ( cut         0.5 0.5 0 ) 
 (1 1 ( 0.5 0.5 )  )
 ( 0.3 0.3 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) 
pplus         ( 0.4 0.4 )  )
;(M1_subcon_subreg pn       metal1       ( cut         0.5 0.5 0 ) 
; (1 1 ( 0.5 0.5 )  )
; ( 0.3 0.3 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) subreg          	(0.4 0.4)
;pplus         ( 0.4 0.4 )  )
;(M1_wellgr        pn           metal1       ( cut         0.5 0.5 0 ) 
; (1 1 ( 0.5 0.5 )  )
; ( 0.15 0.15 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) 
;well          ( 0.25 0.25 )  )
;(M1_dwellcon      pn           metal1       ( cut         0.5 0.5 0 ) 
; (1 1 ( 0.5 0.5 )  )
; ( 0.25 0.25 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) 
;dwell         ( 1 1 )  )
;(M1_dwellgr       pn           metal1       ( cut         0.5 0.5 0 ) 
; (1 1 ( 0.5 0.5 )  )
; ( 0.15 0.15 )  ( 0.3 0.3 )  ( 0 0 )  ( 0 0 )  ( 0 0 ) 
;dwell         ( 0.9 0.9 )  )
) ;standardViaDefs

customViaDefs(
;( viaDefName libName cellName viewName layer1 layer2 resistancePerCut)
;(    ----------    -------     --------     -------       ------ ------     ---------------- )
;( M2_M1            c05_techLib  viaM2M1      via          metal1       metal2       1 )
;( M2_M1_V          c05_techLib  viaM2M1_V    via          metal1       metal2       1 )
;( M2_M1_H          c05_techLib  viaM2M1_H    via          metal1       metal2       1 )
;( M3_M2            c05_techLib  viaM3M2      via          metal2       metal3       1 )
;( M3_M2_V          c05_techLib  viaM3M2_V    via          metal2       metal3       1 )
;( M3_M2_H          c05_techLib  viaM3M2_H    via          metal2       metal3       1 )
( M1_Pdocon        mnsc05prim  viaM1Pdocon  via          pn           metal1       1 )
( M1_Ndocon        mnsc05prim  viaM1Ndocon  via          pn           metal1       1 )
( M1_phvwellcon    mnsc05prim  viaM1phvwellcon via          pn           metal1       1 )
) ;customViaDefs

 ) ;viaDefs

constraintGroups (
;( groupName       [-operator op][-override true|false] //default operator value is precedence, default override value is false;
;( constraintName [layers/lpps]   contraintValue [params] [-isHard true|false] [-comment] )
;( constraintGroup referenceGroupName);
( foundry  nil
 ( constraintGroup leCEConstraintGroup )
 ( minWidth	metal1 	0.6
			 -comment "WIDTH met1 LT 0.6 OUTPUT R60A 30 0" )
( minSpacing	metal1 	0.6
			 -comment "EXT[H] met1 LT 0.6 OUTPUT R60B 30 0 " )

( minWidth	pn 	0.5
			 -comment "minimal width of pn is 0.5u" )
( minSpacing	pn 	0.8
			 -comment "minimal spacing of pn is 0.8u" )

( minWidth	poly1 	0.5
			 -comment "minimal width of poly1 is 0.5u" )
( minSpacing	poly1 	0.5
			 -comment "minimal spacing of poly1 is 0.5u" )
( minWidth	poly0 	0.8
			 -comment "minimal width of poly0 is 0.8u" )
( minSpacing	poly0 	0.9
			 -comment "minimal spacing of poly0 is 0.9u" )
( minWidth	metal2 	0.7
			 -comment "WIDTH met2 LT 0.7 OUTPUT R65A 30 0 " )
( minSpacing	metal2 	0.65
			 -comment "EXT[H] met2 LT 0.65 OUTPUT R65B 30 0 " )
( minWidth	metal3 	0.9
			 -comment "WIDTH met3 LT 0.9 OUTPUT C67A 30 0 " )
( minSpacing	metal3 	0.9
			 -comment "EXT[H] met3 LT 0.9 OUTPUT C67B 30 0 " )
( minClearance poly1 pn 0.3 -comment "40E (5F) Gate poly on thick oxide to active area spacing")
( minClearance cut pn 0.4 -comment "50C (8D) Poly-silicon contact to active area spacing")

( validRoutingLayers	( metal3 via2 metal2 via metal1 cut poly1 poly0 pn ) )
( validRoutingVias      ( M3_M2
                          M2_M1
                          M1_ND
                          M1_PD
                          M1_POLY1
                          M1_wellcon
                          M1_subcon
                          M1_Pdocon
                          M1_Ndocon
                          M1_phvwellcon ) )
);foundry
 ( connectLayers -operator and
  ( leConnectingLayers ( metal3 metal2    ) -byLayer via2 )
  ( leConnectingLayers ( metal2 metal1    ) -byLayer via  )
  ( leConnectingLayers ( metal1 poly1     ) -byLayer cut  )
  ( leConnectingLayers ( metal1 poly0     ) -byLayer cut  )
  ( leConnectingLayers ( metal1 pn        ) -byLayer cut  )
 );connectLayers

( leCEConstraintGroup
( validRoutingLayers	( cut via via2 metal3 metal2 metal1 poly1 poly0 pn ) )
( validRoutingVias      ( M3_M2
                          M2_M1
                          M1_ND
                          M1_PD
                          M1_POLY1
                          M1_wellcon
                          M1_subcon
                          M1_Pdocon
                          M1_Ndocon
                          M1_phvwellcon ) )
);leCEConstraintGroup
( highlightConnectedSetup -operator and
  ( validRoutingLayers ( metal3 via2 metal2 via metal1 cut poly1 poly0 pn ) )
  ( validRoutingVias      ( M3_M2
                            M2_M1
                            M1_ND
                            M1_PD
                            M1_POLY1
                            M1_wellcon
                            M1_subcon
                            M1_Pdocon
                            M1_Ndocon
                            M1_phvwellcon ) )
  ( erasingLayer poly1       ( pn     ))
  ( erasingLayer (re poly1)  ( poly1  ))
  ( erasingLayer (re poly0)  ( poly0  ))
  ( erasingLayer (re pn)     ( pn     ))
  ( erasingLayer (re metal1) ( metal1 ))
  ( erasingLayer (re metal2) ( metal2 ))
  ( erasingLayer (re metal3) ( metal3 ))
  ( leConnectingLayers ( metal3 metal2    ) -byLayer via2 )
  ( leConnectingLayers ( metal2 metal1    ) -byLayer via  )
  ( leConnectingLayers ( metal1 poly1     ) -byLayer cut  )
  ( leConnectingLayers ( metal1 poly0     ) -byLayer cut  )
  ( leConnectingLayers ( metal1 pn        ) -byLayer cut  )
) ; highlightConnectedSetup

) ;constraintGroups

