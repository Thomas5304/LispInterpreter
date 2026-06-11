; macros to read display drf

;; ignore macros
;(print "keywords to ignore" keywords-to-ignore)
(do-list (name keywords-to-ignore)
  (eval
   `(defmacro ,name (&rest args)
      nil)))


(defmacro with-ignore-sub-keywords (names &rest body)
  `(macrolet
       ,(mapcar
          (lambda (name)
            `(,name (&rest params)
                    `(mapcar (lambda (x) x) ',params)))
          names)
     ,@body))



(defun-python handle-define-layer (layer) createLayer displayDRF)
(defun-python handle-define-purpose (purpose) createPurpose displayDRF)


(defun-python handle-define-displayName (name) createDisplay displayDRF)
(defmacro drDefineDisplay (&rest displays)
    `(begin ,@(mapcar ,(lambda (display)
                            (let ((displayName (car display)))
                                (handle-define-displayName displayName)
                                ;0
                            )
                        )
                displays)
    )
)


(defun-python handle-define-linestyle (name display size pattern) createLineStyle displayDRF)
(defmacro drDefineLineStyle (&rest linestyles)
    `(begin ,@(mapcar ,(lambda (linestyle)
                            (let ((display (nth 0 linestyle))
                                    (name (nth 1 linestyle))
                                    (lineSize (nth 2 linestyle))
                                    (linePattern (nth 3 linestyle))
                                )
                                (handle-define-linestyle name display lineSize linePattern )
                                ;0
                            )
                        )
                    linestyles
                )
    )
)

(defun-python handle-define-displaypacket (name display stippleName lineStyleName fillColor outlineColor fillStyle) createDisplayPacket displayDRF)
(defmacro drDefinePacket (&rest packets)
    `(begin ,@(mapcar ,(lambda (packet)
                            (let (
                                (display (nth 0 packet))
                                (name (nth 1 packet))
                                (stippleName (nth 2 packet))
                                (lineStyleName (nth 3 packet))
                                (fillColor (nth 4 packet))
                                (outlineColor (nth 5 packet))
                                (fillStyle (nth 6 packet))
                                )
                                (handle-define-displaypacket name display stippleName lineStyleName fillColor outlineColor fillStyle)
                                ;0
                            )
                        )
                    packets
                )
        )
)

(defun-python handle-define-stipple (name display stipple) createStipple displayDRF)
(defmacro drDefineStipple (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((DisplayName (nth 0 clause))
                             (StippleName (nth 1 clause))
                             (BitMap      (nth 2 clause)))
                         (handle-define-stipple StippleName DisplayName BitMap)
                         ;0
                         )
                       )
                    clauses)
          )
  )

(defun-python handle-define-color (name display red green blue) createColor displayDRF)
(defmacro drDefineColor (&rest colors)
    `(begin ,@(mapcar ,(lambda (color)
                            (let ((display (nth 0 color))
                                (name      (nth 1 color))
                                (Red       (nth 2 color))
                                (Green     (nth 3 color))
                                (Blue      (nth 4 color))
                                (Fill      (nth 5 color))
                                )
                            (handle-define-color name display Red Green Blue )
                            ;0
                            )
                        )
                colors
            )
    )
)

(defmacro dfLayer (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((layerName   (nth 0 clause)))
                            (handle-define-layer layerName)
                            ;0
                        )
                      )
             clauses
            )
    )
  )

(defmacro dfPurpose (&rest clauses)
  `(list ,@(mapcar ,(lambda (clause)
                       (let ((purposeName   (nth 0 clause)))
                            (handle-define-purpose purposeName)
                            ;0
                        )
                      )
             clauses
            )
    )
  )


;;;(defmacro controls (&rest body)
;;;  "Macro zum Parsen des Control-Blocks in einer .tf Datei."
;;;  `(let ((results (make-hash-table)))
;;;     (macrolet (
;;;         ;; Unter-Makro f�r viewTypeUnits
;;;         (viewTypeUnits (&rest units)
;;;           `(let ((mask-entry (assoc 'maskLayout ',units)))
;;;              (when mask-entry
;;;                (setf (gethash 'dbu results) (/ 1.0 (third mask-entry)))
;;;                (setf (gethash 'unit results) (second mask-entry)))))
;;;         
;;;         ;; Unter-Makro f�r mfgGridResolution
;;;         (mfgGridResolution (grid-list)
;;;           `(setf (gethash 'grid results) (caar ',grid-list)))
;;;       )
;;;       ;; F�hre den Inhalt des controls-Blocks aus
;;;       ,@body
;;;       ;; Gib die gesammelten Ergebnisse zur�ck
;;;       (list :dbu (gethash 'dbu results)
;;;             :unit (gethash 'unit results)
;;;             :grid (gethash 'grid results))))
;;;

(defmacro techId (&rest body)
  `(let ((techid-name nil)
         (techid-version nil)
         (techid-revision nil))
     (macrolet (
                (name (parameter)
                      `(setq techid-name ,parameter)
                      )
                (version (parameter)
                         `(setq techid-version ,parameter)
                         )
                
                (revision (parameter)
                          `(setq techid-revision ,parameter)
                          )
                
                )
       ;; F�hre den Inhalt des controls-Blocks aus
       ,@body
       ;(print "techID" techid-name techid-version techid-revision)

        )
       
     ;"techId"
     )
  )

(defun handle-define-control_techParams (name value) 0);(print name "user unit" unitname "DBUPerUU" units))
(defun handle-define-control_viewTypeUnits (name unitname units) 0);(print name "user unit" unitname "DBUPerUU" units))
(defun handle-define-control_mfgGridResolution (grid) 0);(print "mfgGridResolution" grid))



(defmacro controls (&rest body)
  `(let ()
    (with-ignore-sub-keywords (leMPPControls
                                leMPPDefinition
                                leMPPRingObject
                                leMPPMasterPath
                                leMPPEnclosedPath
                                leMPPSubRect)
     (macrolet (
                ;; Unter-Makro f�r viewTypeUnits
                (viewTypeUnits (&rest units)
                               `(mapcar (lambda (unit)
                                          (handle-define-control_viewTypeUnits (nth 0 unit) (nth 1 unit) (nth 2 unit))
                                          )
                                        ',units
                                        )
                               ;`(mapcar (lambda (unit) (let ((a (nth 0 unit))
                               ;                              (b (nth 1 unit))
                               ;                              (c (nth 2 unit)))  (print a c b))) ',units)
                               )
                
                ;; Unter-Makro f�r mfgGridResolution
                (mfgGridResolution (grid-list)
                                   `(handle-define-control_mfgGridResolution ,@grid-list)
                                   )
                (techParams (&rest params)
                                   `(mapcar (lambda (param)
                                          (handle-define-control_techParams (nth 0 param) (nth 1 param))
                                          )
                                        ',params
                                        )
                                   )
                )
       ;; F�hre den Inhalt des controls-Blocks aus
       ,@body
       )
     ;"controls"
     )
    )
  )


(defun handle-define-layerDefinitions_techPurposes (purposeName purposeNum abbreviation) 0)
(defun handle-define-layerDefinitions_techLayers (layerName layerNum abbreviation) 0)
(defun handle-define-layerDefinitions_techLayerPurposePriorities (layerName purposeName) 0)
(defun handle-define-layerDefinitions_techDisplays (layerName purposeName  packet  vis sel   con2ChgLy   drgEnbl  valid) 0)
(defun-python handle-define-layerDefinitions_techDisplays (layerName purposeName  packet  vis sel   con2ChgLy   drgEnbl  valid) createTechDisplays displayDRF)

(defmacro layerDefinitions (&rest body)
  `(let ()
     (macrolet (
                ;; Unter-Makro f�r viewTypeUnits
                (techPurposes (&rest purposes)
                              `(mapcar
                                (lambda (purpose)
                                  (handle-define-layerDefinitions_techPurposes (nth 0 purpose) (nth 1 purpose) (nth 2 purpose))
                                  )
                                 ',purposes))
                
                ;; Unter-Makro f�r techLayers
                (techLayers (&rest layers)
                            `(mapcar
                                (lambda (layer)
                                  (handle-define-layerDefinitions_techLayers (nth 0 layer) (nth 1 layer) (nth 2 layer))
                                  )
                                 ',layers))

                ;; Unter-Makro f�r techLayerPurposePriorities
                (techLayerPurposePriorities (&rest prios)
                            `(mapcar
                                (lambda (prio)
                                  (handle-define-layerDefinitions_techLayerPurposePriorities (nth 0 prio) (nth 1 prio))
                                  )
                                 ',prios))
                
                ;; Unter-Makro f�r techDisplays
                (techDisplays (&rest displays)
                              `(mapcar
                                (lambda (display)
                                  (handle-define-layerDefinitions_techDisplays  (nth 0 display) (nth 1 display) (nth 2 display) (nth 3 display)
                                                                                (nth 4 display) (nth 5 display) (nth 6 display) (nth 8 display))
                                )
                                ',displays))
                )
       ;; F�hre den Inhalt des controls-Blocks aus
       ,@body
       )
     ;"layerDefinitions"
     )
  )



(defun handle-define-layerRules_functions (layer function maskNumber ) 0)
(defun handle-define-layerRules_mfgResolutions (layer mfgResolution ) 0) 
    

(defmacro layerRules (&rest body)
  `(let ()
     (macrolet (
                ;; Unter-Makro f�r functions
                (functions (&rest functions)
                               `(mapcar
                                  (lambda (function)
                                    (handle-define-layerRules_functions (nth 0 function) (nth 1 function) (if (>= (length function) 3) (nth 2 function) nil))
                                    )
                                  ',functions))
                
                ;; Unter-Makro f�r mfgResolutions
                (mfgResolutions (&rest resolutions)
                                `(mapcar
                                  (lambda (resolution)
                                    (handle-define-layerRules_mfgResolutions (nth 0 resolution) (nth 1 resolution))
                                    )
                                  ',resolutions))
                )
                
       ;; F�hre den Inhalt des controls-Blocks aus
       ,@body
       )
     ;"layerRules"
     )
  )


(defun load-display-drf (displayDRF)
  (begin
   (print (+ "reading DRF file " displayDRF))
   (let ((function-mode t))
     (include displayDRF)
     )
   )
)

(defun load-techfile-tf (techfile-tf)
  (begin
   (print (+ "reading TF file " techfile-tf))
   (let ((function-mode t))
     (include techfile-tf)
     )
   )
  )
