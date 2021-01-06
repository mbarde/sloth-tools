class JobQueue {

  constructor(maxJobCount) {
    this.jobs = []
    this.maxJobCount = maxJobCount

    /* callbacks */
    this.onJobDone = null
    this.onAllJobsDone = null
  }

  addJob(promise) {
    if (this.jobs.length >= this.maxJobCount) return
    this.jobs.push(promise)
    if (this.jobs.length === 1) this.callNext()
  }

  callNext() {
    if (this.jobs.length === 0) {
      if (this.onAllJobsDone !== null) this.onAllJobsDone()
      return
    }
    this.jobs[0]().then(() => {
      this.jobs.shift()  // remove first item
      if (this.onJobDone !== null) this.onJobDone()
      this.callNext()
    })
  }

  getJobCount() {
    return this.jobs.length
  }

}
