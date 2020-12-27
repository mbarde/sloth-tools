class JobQueue {

  constructor(maxJobCount) {
    this.jobs = []
    this.maxJobCount = maxJobCount
  }

  addJob(promise) {
    if (this.jobs.length >= this.maxJobCount) return
    console.log('job added')
    this.jobs.push(promise)
    console.log(this.jobs)
    if (this.jobs.length === 1) this.callNext()
  }

  callNext() {
    if (this.jobs.length === 0) {
      console.log('done!')
      return
    }
    console.log('next job ...')
    console.log(this.jobs[0])
    this.jobs[0]().then(() => {
      this.jobs.shift()  // remove first item
      this.callNext()
    })
  }

}
