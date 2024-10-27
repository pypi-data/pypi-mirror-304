#! /usr/bin/env bash

function CV_build() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        local options="${EOP}dryrun,~publish,~rm,what=<cv+cv-full>$EOPE"
        local latex_options=$EOP$abcli_latex_build_options$EOPE
        abcli_show_usage "CV build$ABCUL$options$ABCUL$latex_options" \
            "build CV."
        return
    fi

    local latex_options=$2

    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_publish=$(abcli_option_int "$options" publish $(abcli_not $do_dryrun))
    local do_rm=$(abcli_option_int "$options" rm 1)
    local what=$(abcli_option "$options" what cv+cv-full)

    abcli_log "building CV... [$what]"

    pushd $abcli_path_git/CV/src >/dev/null

    python3 -m abadpour build

    local filename
    local public_filename
    for filename in $(echo $what | tr + " "); do
        abcli_latex build dryrun=$do_dryrun,$latex_options \
            ./$filename.tex

        if [[ "$do_publish" == 1 ]]; then
            public_filename=arash-abadpour-resume
            [[ "$filename" == *"full"* ]] && public_filename=$public_filename-full

            abcli_eval dryrun=$do_dryrun \
                aws s3 cp \
                $filename.pdf \
                s3://abadpour-com/cv/$public_filename.pdf
        fi

        [[ "$do_rm" == 1 ]] && rm -v $filename.pdf

    done

    popd >/dev/null
}
