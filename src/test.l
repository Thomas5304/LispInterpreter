(defun-python handle-define-stipple (name display stipple) createStipple displayDRF)
(defmacro drDefineStipple (&rest clauses)
  `(begin ,@(mapcar (lambda (clause)
                       (let ((DisplayName (nth 0 clause))
                             (StippleName (nth 1 clause))
                             (BitMap      (nth 2 clause)))
                         `(handle-define-stipple ',StippleName
                                                 ',DisplayName
                                                 ',BitMap)
                         ;0
                         )
                       )
                    clauses)
          )

  )

(defun-python handle-define-layer (layer) createLayer displayDRF)
(defmacro dfLayer (&rest clauses)
  `(begin ,@(mapcar (lambda (clause)
                        (let ((layerName   (nth 0 clause)))
                            `(handle-define-layer ',layerName)
                            ;0
                        )
                      )
              clauses
            )
    )
  )

(defun-python handle-define-purpose (purpose) createPurpose displayDRF)
(defmacro dfPurpose (&rest clauses)
  `(begin ,@(mapcar (lambda (clause)
                        (let ((purposeName   (nth 0 clause)))
                            `(handle-define-purpose ',purposeName)
                            ;0
                        )
                      )
              clauses
            )
    )
  )

(print "load display.drf")
(let ((function-mode t))
 (load "small.display.drf")
  )
  (quit)