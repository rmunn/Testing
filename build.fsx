#r "paket: 
nuget Fake.Core.Target //"

#load "./.fake/build.fsx/intellisense.fsx"

open Fake.Core

Target.create "Hello" (fun _ ->
    Trace.tracefn "Hello from FAKE build process!"
)

Target.runOrDefault "Hello"
