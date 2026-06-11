
(setq indent 0)

(defun make-indentation (spc)
  (if (== spc 0) "" (+ (make-indentation (1- spc)) " ")))

(defmacro print-indent (&rest print-items)
  `(print (make-indentation indent) ,@print-items)
  )

(defun make-attr-assign (id-vals)
  (+ (if (> (length id-vals) 1)
         (+ " " (nth 0 id-vals) "=" (nth 1 id-vals)
            (make-attr-assign (cdr (cdr id-vals)))
            )
       
       " "))
    )


;(defmacro xml (key-attr &rest body)
;  `(let* ((data ',key-attr)
;         (key (if (list? data) (car data) data))
;         (attr (if (list? data) (cdr data) '()))
;         )
;     (print-indent (+ "<" key ,@(make-attr-assign attr) ">"))
;     (let* ((indent (+ indent 2))
;           )
;       ,@body
;       )
;     (print-indent (+ "</" key ">"))
;     )
;  )
                                        ;
(defmacro xml (key-attr &rest body)
  (let* ((is-list (list? key-attr))
         (tag (if is-list (car key-attr) key-attr))
         (attr-elements (if is-list (cdr key-attr) '())))
    `(let ((key ,tag)
           ;; Wir erstellen zur Laufzeit eine Liste aus den Attributen
           (attr (list ,@attr-elements))) 
       (print-indent (+ "<" key (make-attr-assign attr) ">"))
       (let ((indent (+ indent 2)))
         ,@body)
       (print-indent (+ "</" key ">")))))

(mk-counter next-id)

(xml ("test" "id" (next-id++))
     (xml ("level1" "id" (next-id++))
          (xml ("level2" "id" (next-id++))
               (print-indent "text" )
               )
          )
     )

