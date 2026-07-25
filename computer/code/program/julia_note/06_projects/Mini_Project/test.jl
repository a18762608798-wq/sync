# this file use to test the environment of the project, and make sure all the dependencies are installed correctly.
function main()
    return println("Hello, World!")
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
