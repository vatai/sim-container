((dockerfile-mode
  .
  ((eval . (setq
            dockerfile-build-args
            (mapcar
             (lambda (input)
               (format "%s=%s"
                       (car input)
                       (substring
                        (shell-command-to-string (cadr input))
                        0 -1)))
             '(("USER_ID" "id -u")
               ("USER" "id -un")
               ("GROUP_ID" "id -g")
               ("GROUP" "id -gn"))))))))
