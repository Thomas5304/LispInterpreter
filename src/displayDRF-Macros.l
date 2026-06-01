; macros to read display drf


;interfaces to python
(defun-python handle-define-stipple (name display stipple) createStipple displayDRF)
(defun-python handle-define-lpp (layer purpose (&optional stippleName)) createLPP displayDRF)
(defun-python handle-define-layer (layer) createLayer displayDRF)
(defun-python handle-define-purpose (purpose) createPurpose displayDRF)
(defun-python handle-define-linestyle (name display size pattern) createLineStyle displayDRF)
(defun-python handle-define-displayName (name) createDisplay displayDRF)
(defun-python handle-define-color (name display red green blue) createColor displayDRF)
(defun-python handle-define-displaypacket (name display stippleName lineStyleName fillColor outlineColor fillStyle) createDisplayPacket displayDRF)




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

(defmacro drDefineColor (&rest colors)
    `(begin ,@(mapcar ,(lambda (color)
                            (let ((DisplayName (nth 0 color))
                                    (ColorName (nth 1 color))
                                    (Red (nth 2 color))
                                    (Green (nth 3 color))
                                    (Blue (nth 4 color))
                                )
                                ;(print "Color for display "  DisplayName " -> " ColorName "  (" Red Green Blue ")" )
                                0
                            )
                        )
                    colors
                )
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

(defmacro dfLayerTable (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((layerName   (nth 0 clause))
                             (purposeName (nth 1 clause))
                             (stippleName (if (>= (length clause) 3)
                                          (nth 2 clause)
                                          ""))
                            )
                            ;(handle-define-lpp layerName purposeName stippleName)
                            0
                        )
                      )
             clauses
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


(defun load-display-drf (displayDRF)
    (let ((function-mode t))
        (include displayDRF)
    )
)
