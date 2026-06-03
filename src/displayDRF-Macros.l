; macros to read display drf


;interfaces to python
(defun-python handle-define-stipple (name display stipple) createStipple displayDRF)
(defun-python handle-define-linestyle (name display size pattern) createLineStyle displayDRF)
(defun-python handle-define-displayName (name) createDisplay displayDRF)
(defun-python handle-define-color (name display red green blue) createColor displayDRF)
(defun-python handle-define-displaypacket (name display stippleName lineStyleName fillColor outlineColor fillStyle) createDisplayPacket displayDRF)


(defun-python handle-define-layer (layer) createLayer displayDRF)
(defun-python handle-define-purpose (purpose) createPurpose displayDRF)


(defmacro ignore (&rest clauses)
    0
)


(defmacro drDefineDisplay (&rest displays)
    `(begin ,@(mapcar ,(lambda (display)
                            (let ((displayName (car display)))
                                (handle-define-displayName displayName)
                                0
                            )
                        )
                displays)
    )
)


(defmacro drDefineLineStyle (&rest linestyles)
    `(begin ,@(mapcar ,(lambda (linestyle)
                            (let ((display (nth 0 linestyle))
                                    (name (nth 1 linestyle))
                                    (lineSize (nth 2 linestyle))
                                    (linePattern (nth 3 linestyle))
                                )
                                (handle-define-linestyle name display lineSize linePattern )
                                0
                            )
                        )
                    linestyles
                )
    )
)

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
                                0
                            )
                        )
                    packets
                )
        )
)

(defmacro drDefineStipple (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((DisplayName (nth 0 clause))
                             (StippleName (nth 1 clause))
                             (BitMap      (nth 2 clause)))
                         (handle-define-stipple StippleName DisplayName BitMap)
                         0
                         )
                       )
                    clauses)
          )
  )

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
                            0
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
                            0
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
                            0
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
;;;         ;; Unter-Makro für viewTypeUnits
;;;         (viewTypeUnits (&rest units)
;;;           `(let ((mask-entry (assoc 'maskLayout ',units)))
;;;              (when mask-entry
;;;                (setf (gethash 'dbu results) (/ 1.0 (third mask-entry)))
;;;                (setf (gethash 'unit results) (second mask-entry)))))
;;;         
;;;         ;; Unter-Makro für mfgGridResolution
;;;         (mfgGridResolution (grid-list)
;;;           `(setf (gethash 'grid results) (caar ',grid-list)))
;;;       )
;;;       ;; Führe den Inhalt des controls-Blocks aus
;;;       ,@body
;;;       ;; Gib die gesammelten Ergebnisse zurück
;;;       (list :dbu (gethash 'dbu results)
;;;             :unit (gethash 'unit results)
;;;             :grid (gethash 'grid results))))
;;;

(defmacro controls (&rest body)
  `(let ()
     (macrolet (
                ;; Unter-Makro für viewTypeUnits
                (viewTypeUnits (&rest units)
                               `(mapcar (lambda (unit)
                                          (when (== (nth 0 unit) "maskLayout")
                                            (print "masklayout " (nth 2 unit) (nth 1 unit))
                                            )
                                          )
                                        ',units
                                        )
                               ;`(mapcar (lambda (unit) (let ((a (nth 0 unit))
                               ;                              (b (nth 1 unit))
                               ;                              (c (nth 2 unit)))  (print a c b))) ',units)
                               )
                
                ;; Unter-Makro für mfgGridResolution
                (mfgGridResolution (grid-list)
                                   `(print ,@grid-list)
                                   )
                )
       ;; Führe den Inhalt des controls-Blocks aus
       ,@body
       )
     )
  )

(defmacro layerDefinitions (&rest body)
  `(let ()
     (macrolet (
                ;; Unter-Makro für viewTypeUnits
                (techPurposes (&rest params)
                               `(print ',params))
                
                ;; Unter-Makro für techLayers
                (techLayers (&rest params)
                            `(print ',params))

                ;; Unter-Makro für techLayerPurposePriorities
                (techLayerPurposePriorities (&rest params)
                            `(print ',params))
                
                ;; Unter-Makro für techDisplays
                (techDisplays (&rest params)
                            `(print ',params))
                )
                
       ;; Führe den Inhalt des controls-Blocks aus
       ,@body
       )
     )
  )


(defmacro layerRules (&rest body)
  `(let ()
     (macrolet (
                ;; Unter-Makro für functions
                (functions (&rest params)
                               `(print ',params))
                
                ;; Unter-Makro für mfgResolutions
                (mfgResolutions (&rest params)
                            `(print ',params))
                )
                
       ;; Führe den Inhalt des controls-Blocks aus
       ,@body
       )
     )
  )



(defun load-display-drf (displayDRF)
    (let ((function-mode t))
        (include displayDRF)
    )
)

(defun load-techfile-tf (techfile-tf)
    (let ((function-mode t))
        (include techfile-tf)
    )
)
